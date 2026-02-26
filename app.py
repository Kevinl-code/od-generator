from flask import Flask, render_template, jsonify, request
import pandas as pd
import uuid, json, os
from datetime import datetime

app = Flask(__name__)
DB_FILE = "od_records.json"

def load_students():
    try:
        df = pd.read_excel("students.xlsx")
    except:
        df = pd.read_csv("students.csv")
    return df.to_dict(orient="records")

def load_od_records():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_od_record(data):
    db = load_od_records()
    od_id = str(uuid.uuid4())[:8]
    data["timestamp"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    db[od_id] = data

    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

    return od_id

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_students")
def get_students():
    return jsonify(load_students())

@app.route("/save_od", methods=["POST"])
def save_od():
    data = request.json
    od_id = save_od_record(data)
    return jsonify({"od_id": od_id})

@app.route("/verify/<od_id>")
def verify(od_id):
    db = load_od_records()
    record = db.get(od_id)
    return render_template("verify.html", record=record, od_id=od_id)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
