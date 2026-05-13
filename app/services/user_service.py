from typing import Dict, Optional
from ..database.connection import Database

class UserService:
    def __init__(self):
        self.db = Database.connect()

    def create_user(self, user_data: Dict) -> str:

        if "role" not in user_data:
            user_data["role"] = "citizen"
        
        result = self.db.users.insert_one(user_data)
        return str(result.inserted_id)

    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        return self.db.users.find_one({"userId": user_id}, {"_id": 0})

    def update_user_profile(self, user_id: str, updates: Dict):
        self.db.users.update_one(
            {"userId": user_id},
            {"$set": updates}
        )

    def verify_role(self, user_id: str, required_role: str) -> bool:
        user = self.get_user_by_id(user_id)
        return user and user.get("role") == required_role