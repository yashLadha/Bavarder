from pymongo import MongoClient


class MongoConn:

    client = None
    db = None
    user_coll = None

    def __init__(self):
        MongoConn.client = MongoClient()
        MongoConn.db = MongoConn.client['bavarder']
        MongoConn.user_coll = MongoConn.db['users']

    @staticmethod
    def get_user_collection():
        return MongoConn.user_coll

    @staticmethod
    def create_database():
        client = MongoConn()
        return client

    @staticmethod
    def check_database():
        if MongoConn.get_user_collection() is None:
            MongoConn.create_database()
            if MongoConn.get_user_collection() is None:
                print('Unable to create database Object')
                return False
            else:
                return True
        else:
            print('MongoConn object already exists.')
            return True
