CUSTOMER_PROFILES = {
    "default": {
        "vt_weight": 1.0,
        "abuse_weight": 1.0,
        "score_cap": 60,
        "category_overrides": {}
    },

    "banking": {
        "vt_weight": 0.7,
        "abuse_weight": 1.6,
        "score_cap": 70,
        "category_overrides": {
            "auth": {"vt": 0.4, "abuse": 1.8},
            "network": {"vt": 1.5, "abuse": 0.6}
        }
    },

    "saas": {
        "vt_weight": 1.3,
        "abuse_weight": 1.0,
        "score_cap": 60,
        "category_overrides": {
            "auth": {"vt": 0.6, "abuse": 1.4}
        }
    }
}


def get_customer_profile(customer_id: str | None):
    return CUSTOMER_PROFILES.get(customer_id, CUSTOMER_PROFILES["default"])
