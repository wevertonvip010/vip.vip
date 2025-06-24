from pymongo import MongoClient
from src.config import Config
import logging

class Database:
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            try:
                self._client = MongoClient(Config.MONGODB_URI)
                # Extrair nome do banco da URI ou usar padrão
                db_name = Config.MONGODB_URI.split('/')[-1] if '/' in Config.MONGODB_URI else 'vip_mudancas'
                self._db = self._client[db_name]
                
                # Testar conexão
                self._client.admin.command('ping')
                logging.info(f"Conectado ao MongoDB: {db_name}")
                
            except Exception as e:
                logging.error(f"Erro ao conectar com MongoDB: {e}")
                # Fallback para MongoDB local
                self._client = MongoClient('mongodb://localhost:27017/')
                self._db = self._client['vip_mudancas']
    
    @property
    def db(self):
        return self._db
    
    @property
    def client(self):
        return self._client
    
    def close(self):
        if self._client:
            self._client.close()

# Instância global do banco
db = Database().db

