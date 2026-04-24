from flask import Flask, jsonify
from pymongo import MongoClient, errors

app = Flask(__name__)

# 🔗 Настройки (как просили, без .env)
MONGO_URI = "mongodb+srv://admin:123456qwerty@cluster0.mvdyb6h.mongodb.net/?appName=Cluster0"
DB_NAME = "bot"
COLLECTION_NAME = "users"

# Подключение к MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db[COLLECTION_NAME]

@app.route("/count", methods=["GET"])
def count_users():
    try:
        # count_documents({}) считает все записи (документы) в коллекции
        total = users_collection.count_documents({})
        return jsonify({
            "db": DB_NAME,
            "collection": COLLECTION_NAME,
            "total_records": total
        }), 200
    except errors.PyMongoError as e:
        return jsonify({"error": f"Ошибка MongoDB: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True
