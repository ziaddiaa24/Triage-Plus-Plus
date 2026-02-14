from sklearn.ensemble import IsolationForest

class BehaviorModel:
    def __init__(self):
        self.model = IsolationForest(
            n_estimators=200,
            contamination=0.05,
            random_state=42
        )
        self.fitted = False

    def train(self, feature_df):
        X = feature_df[
            ["avg_alert_hour", "alert_count", "distinct_source_ips"]
        ]
        self.model.fit(X)
        self.fitted = True

    def score(self, feature_row):
        X = feature_row[
            ["avg_alert_hour", "alert_count", "distinct_source_ips"]
        ]

        score = self.model.decision_function(X)[0]
        label = self.model.predict(X)[0]

        status = "normal" if label == 1 else "suspicious"

        return score, status
