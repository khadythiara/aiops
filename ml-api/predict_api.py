from flask import Flask, request, jsonify
from sklearn.ensemble import IsolationForest
import pandas as pd
import os, json

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    log_path = "./logs/app.log"
    if not os.path.exists(log_path):
        return jsonify({"error": "log file not found"}), 404

    with open(log_path) as f:
        lines = f.readlines()

    timestamps = [i for i in range(len(lines))]
    df = pd.DataFrame({"timestamp": timestamps})
    model = IsolationForest(contamination=0.2, random_state=42)
    df["anomaly"] = model.fit_predict(df[["timestamp"]])

    anomalies = df[df["anomaly"] == -1]
    anomaly_json = [
        {"timestamp": int(row["timestamp"]), "anomaly": True}
        for _, row in anomalies.iterrows()
    ]

    with open("./logs/anomalies.json", "w") as out:
        for line in anomaly_json:
            out.write(json.dumps(line) + "\n")

    return jsonify({"detected": len(anomalies)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
