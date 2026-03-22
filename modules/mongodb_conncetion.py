from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


class MongoDBConnectionHandler:
    def __init__(self) -> None:
        self.__connection = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    
    def valid_connection(self) -> MongoClient | None:
        try:
            self.__connection.admin.command('ping')
            self.__connection.server_info()
            print("Conexão com o MongoDB estabelecida com sucesso!")
            return self.__connection  
        except ServerSelectionTimeoutError:
            print("❌ Timeout — MongoDB não encontrado ou fora do ar")
        except ConnectionFailure:
            print("❌ Falha na conexão com o MongoDB")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
        return None