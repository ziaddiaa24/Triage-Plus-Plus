def explain(alert, rep, behavior, intel, risk, proba):
    reasons = []

    if intel > 0:
        reasons.append(f"Threat Intel reports malicious IP (score +{intel})")

    if rep < 0:
        reasons.append(f"High repetition detected (noise reduction {rep})")

    if behavior > 0:
        reasons.append(f"Behavior deviates from baseline (+{behavior})")
    else:
        reasons.append("Behavior matches historical baseline")

    reasons.append(f"Computed risk score = {risk}")
    reasons.append(f"ML confidence of real attack = {round(proba,3)}")

    if proba < 0.3:
        reasons.append("ML model classifies this as likely false positive")
    elif proba > 0.8:
        reasons.append("ML model is highly confident this is a real attack")
    else:
        reasons.append("ML model is uncertain — requires human review")

    return reasons
