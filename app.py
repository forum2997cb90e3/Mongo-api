from pymongo import MongoClient
import json

# Замените на вашу строку подключения
uri = "mongodb+srv://admin:123456qwerty@cluster0.mvdyb6h.mongodb.net/?appName=Cluster0"

def get_all_users():
    client = MongoClient(uri)
    
    try:
        db = client["bot"]
        collection = db["users"]
        
        # Получить все документы
        users = collection.find({})
        
        print("Все пользователи:\n")
        for user in users:
            user['_id'] = str(user['_id'])  # ObjectId не сериализуется в JSON
            print(json.dumps(user, indent=2, ensure_ascii=False))
            print("---")
            
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    get_all_users()
