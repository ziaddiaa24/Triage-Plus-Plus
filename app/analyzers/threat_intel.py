import os
import requests
from app.core.customer_profiles import get_customer_profile

VT_API_KEY = os.getenv("VT_API_KEY")
ABUSEIPDB_API_KEY = (
    os.getenv("ABUSEIPDB_API_KEY")
    or "e438faffc913b7db93121963458da4e26c0f966d3840a9830c2d055e7af6a519431c4c39a1663d67"
)

# ===============================
# CATEGORY WEIGHTS
# ===============================

CATEGORY_WEIGHTS = {
    "auth": {
        "abuse": 1.5,
        "vt": 0.6
    },
    "network": {
        "abuse": 0.7,
        "vt": 1.4
    },
    "endpoint": {
        "abuse": 1.0,
        "vt": 1.0
    },
    "generic": {
        "abuse": 1.0,
        "vt": 1.0
    }
}

# ===============================
# VirusTotal
# ===============================

def _virustotal_lookup(ip: str):
    if not VT_API_KEY:
        return 0, "VirusTotal disabled", "neutral"

    try:
        r = requests.get(
            f"https://www.virustotal.com/api/v3/ip_addresses/{ip}",
            headers={"x-apikey": VT_API_KEY},
            timeout=5
        )

        if r.status_code != 200:
            return 0, "VirusTotal error", "neutral"

        stats = r.json()["data"]["attributes"]["last_analysis_stats"]
        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)

        score = min((malicious * 15) + (suspicious * 7), 40)

        if score == 0:
            return 0, "VirusTotal clean", "neutral"

        return score, f"VirusTotal: {malicious} malicious, {suspicious} suspicious", "high"

    except Exception:
        return 0, "VirusTotal unreachable", "neutral"


# ===============================
# AbuseIPDB
# ===============================

def _abuseipdb_lookup(ip: str):
    if not ABUSEIPDB_API_KEY:
        return 0, "AbuseIPDB disabled", "neutral"

    try:
        r = requests.get(
            "https://api.abuseipdb.com/api/v2/check",
            headers={
                "Key": ABUSEIPDB_API_KEY,
                "Accept": "application/json"
            },
            params={
                "ipAddress": ip,
                "maxAgeInDays": 90
            },
            timeout=5
        )

        if r.status_code != 200:
            return 0, "AbuseIPDB error", "neutral"

        data = r.json()["data"]
        confidence = data.get("abuseConfidenceScore", 0)
        reports = data.get("totalReports", 0)

        score = min(confidence, 40)

        if score == 0:
            return 0, "AbuseIPDB clean", "neutral"

        return score, f"AbuseIPDB: {confidence}% confidence ({reports} reports)", "high"

    except Exception:
        return 0, "AbuseIPDB unreachable", "neutral"


# ===============================
# Combined Threat Intel
# ===============================

def vt_ip_score(ip: str, category: str = "generic", customer_id: str | None = None):
    profile = get_customer_profile(customer_id)

    vt_score, vt_msg, _ = _virustotal_lookup(ip)
    abuse_score, abuse_msg, _ = _abuseipdb_lookup(ip)

    vt_weight = profile["vt_weight"]
    abuse_weight = profile["abuse_weight"]

    # Category override (if exists)
    if category in profile.get("category_overrides", {}):
        override = profile["category_overrides"][category]
        vt_weight = override.get("vt", vt_weight)
        abuse_weight = override.get("abuse", abuse_weight)

    weighted_vt = vt_score * vt_weight
    weighted_abuse = abuse_score * abuse_weight

    final_score = min(
        int(weighted_vt + weighted_abuse),
        profile.get("score_cap", 60)
    )

    if final_score >= 40:
        impact = "high"
    elif final_score >= 20:
        impact = "medium"
    elif final_score > 0:
        impact = "low"
    else:
        impact = "neutral"

    messages = []
    if abuse_score > 0:
        messages.append(abuse_msg)
    if vt_score > 0:
        messages.append(vt_msg)

    message = " | ".join(messages) if messages else "No threat intelligence signals"

    return final_score, message, impact
