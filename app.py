from flask import Flask, jsonify
from pymongo import MongoClient, errors

app = Flask(__name__)

# 🔗 Прямое подключение (без .env)
client = MongoClient("mongodb+srv://admin:123456qwerty@cluster0.mvdyb6h.mongodb.net/?appName=Cluster0")
db = client["bot"]
users_col = db["users"]

@app.route("/users/count", methods=["GET"])
def count_users():
    try:
        total = users_col.count_documents({})
        return jsonify({"total_users": total}), 200
    except errors.PyMongoError as e:
        return jsonify({"error": f"DB error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
