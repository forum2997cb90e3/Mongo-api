from flask import Flask, jsonify
from pymongo import MongoClient, errors
from bson import ObjectId

app = Flask(__name__)

# 🔗 Настройки (без .env)
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "bot"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_col = db["users"]
bans_col = db["bans"]

def to_json(doc):
    """Рекурсивно преобразует MongoDB-типы (ObjectId, datetime) в строки для JSON"""
    result = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            result[key] = str(value)
        elif isinstance(value, dict):
            result[key] = to_json(value)
        else:
            result[key] = value
    return result

@app.route("/count", methods=["GET"])
def get_counts():
    try:
        return jsonify({
            "db": DB_NAME,
            "counts": {
                "users": users_col.count_documents({}),
                "bans": bans_col.count_documents({})
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/bans", methods=["GET"])
def get_all_bans():
    try:
        # Получаем все документы из коллекции
        raw_bans = list(bans_col.find())
        # Преобразуем в JSON-совместимый формат
        bans_data = [to_json(doc) for doc in raw_bans]
        
        return jsonify({
            "collection": "bans",
            "total": len(bans_data),
            "data": bans_data
        }), 200
    except errors.PyMongoError as e:
        return jsonify({"error": f"Ошибка MongoDB: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
