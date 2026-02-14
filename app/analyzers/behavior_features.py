import pandas as pd

def extract_features(alerts):
    """
    alerts: list of dicts
    """
    df = pd.DataFrame(alerts)

    df["@timestamp"] = pd.to_datetime(df["@timestamp"])
    df["alert_hour"] = df["@timestamp"].dt.hour

    features = df.groupby("user").agg(
        avg_alert_hour=("alert_hour", "mean"),
        alert_count=("alert_hour", "count"),
        distinct_source_ips=("source_ip", "nunique")
    ).reset_index()

    return features
