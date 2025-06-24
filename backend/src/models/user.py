from bson import ObjectId
from src.database import db
import bcrypt
from datetime import datetime

class User:
    collection = db.users
    
    @staticmethod
    def create_user(email, password, name, role='admin'):
        """Criar novo usuário"""
        # Verificar se usuário já existe
        if User.collection.find_one({"email": email}):
            return None
        
        # Hash da senha
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user_data = {
            "email": email,
            "password": password_hash,
            "name": name,
            "role": role,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "active": True
        }
        
        result = User.collection.insert_one(user_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_email(email):
        """Buscar usuário por email"""
        return User.collection.find_one({"email": email})
    
    @staticmethod
    def find_by_id(user_id):
        """Buscar usuário por ID"""
        return User.collection.find_one({"_id": ObjectId(user_id)})
    
    @staticmethod
    def verify_password(password, password_hash):
        """Verificar senha"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash)
    
    @staticmethod
    def to_dict(user_doc):
        """Converter documento do MongoDB para dict"""
        if not user_doc:
            return None
        
        return {
            'id': str(user_doc['_id']),
            'email': user_doc['email'],
            'name': user_doc['name'],
            'role': user_doc['role'],
            'active': user_doc.get('active', True),
            'created_at': user_doc.get('created_at'),
            'updated_at': user_doc.get('updated_at')
        }
