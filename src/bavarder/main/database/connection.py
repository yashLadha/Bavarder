import datetime

from pymongo import MongoClient
import gridfs


class MongoConn:
    """Mongo DB Helper"""
    client = None
    db = None
    user_coll = None
    fs = None

    def __init__(self):
        MongoConn.client = MongoClient()
        MongoConn.db = MongoConn.client['bavarder']
        MongoConn.user_coll = MongoConn.db['users']
        MongoConn.fs = gridfs.GridFS(MongoConn.db, 'users')

    @staticmethod
    def get_user_collection():
        """
        Getter method for retrieving the user collection.
        :return: User collection object
        """
        return MongoConn.user_coll

    @staticmethod
    def get_image(id):
        return MongoConn.fs.get(id)

    @staticmethod
    def create_database():
        """
        Creates database instance in the Mongo shell.
        :return: Database object created
        """
        client = MongoConn()
        return client

    @staticmethod
    def insert_image(file, user):
        """Method to upload the profile image in the mongo db."""
        file_res = MongoConn.fs.put(file, filename=user['email'])
        MongoConn.user_coll.update_one({'_id': user['_id']}, {"$set": {'image': file_res}}, upsert=False)
        return file_res

    @staticmethod
    def check_database():
        """
        Method to the check the database is already present
        or not. It also checks the user collection is
        present or not, in the database.
        :return: Flag for the existence of database in the mongo
        shell along with the presence of user collection object.
        """
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

    @staticmethod
    def create_user(email, password, name, dob):
        """
        Method to create the user in the Mongo Database.
        Method returns the result and the result code.
        Result code specifies the condition flags for
        the result obtained. Like used to specify the
        reason for the result.
        :param email: email of the user
        :param password: password of the user
        :param name: name of the user
        :param dob: date of birth of the user
        :return: result and result code
        """
        if MongoConn.check_database():
            user_coll = MongoConn.user_coll
            cursor = list(user_coll.find({'email': email}, {'_id': 1}))
            if len(cursor) > 0:
                print('User with same email already exists.')
                return False, -2
            result = user_coll.insert_one({
                "email": email,
                "password": password,
                "name": name,
                "dob": datetime.datetime.strptime(str(dob), "%Y-%m-%d")
            })
            if result.inserted_id is not None:
                print('User inserted successfully.')
                return True, 0
            else:
                print('Unable to insert the User.')
                return False, -1
        else:
            return False, -1

    @staticmethod
    def is_user(email, password):
        """
        Method for checking the existence of user in the
        database.
        :param email: email of the user
        :param password: password of the user
        :return: It returns the flag for the existence of
        the user in the database i.e. user is present in the
        database (True) or not (False).
        """
        if MongoConn.check_database():
            user_instance = MongoConn.get_user(email)
            if user_instance:
                if user_instance['password'] == password:
                    print('User exists')
                    return True, user_instance
            else:
                print('User doesn\'t exists')
                return False, None
        else:
            return False

    @staticmethod
    def get_user(email):
        """Method for getting the user from the MongoDB database

        Args:
            email: str. Email of the user.
        """
        if MongoConn.check_database():
            user_coll = MongoConn.user_coll
            cursor = user_coll.find({'email': email})
            for user in cursor:
                return user
