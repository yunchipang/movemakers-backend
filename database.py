from pymongo import MongoClient
import settings

client = MongoClient(settings.mongodb_uri, settings.mongodb_port)
db = client["movemakers"]