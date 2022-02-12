from flask_restful import Resource
from flask import request
import random
import string
from backend.backend_app.common.db import SqliteDBMS

DATA_PATH = '../data/WinNBQ.db3'


class UsersRegister(Resource):
    def get(self):
        pass

    def post(self):
        dbms = SqliteDBMS(DATA_PATH)
        data = request.get_json()

        username = data["username"]
        password = data["password"]
        email = data["email"]
        birthday = data["birthday"]
        gender = data["gender"]

        while(True):
            id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(20)])
            query_str = "select * from User where id ='"+id+"'"

            # select * from table where id = fetched id (here id)

            obj = dbms.query(query_str)

            if obj[1] == []:
                break
            continue
        query_str_username = "select * from User where username ='"+username+"'"
        obj1 = dbms.query(query_str_username)
        query_str_email = "select * from User where email ='"+email+"'"
        obj2 = dbms.query(query_str_email)

        if obj1[1] != [] or obj2[1] != [] :
            # json conversion required
            return " Invalid username or email"

        table = 'User'
        col_to_val = {
            "id": id,
            "username": username ,
            "password": password ,
            "email": email ,
            "birthday": birthday,
            "gender": gender,
        }

        dbms.add(table,col_to_val)

        return "hello"

        pass


class UsersLogin(Resource):
    def get(self):


        pass

    def post(self):

        dbms = SqliteDBMS(DATA_PATH)
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        query_str = "select * from User where username = '"+username+"' and password ='"+password+"'"
        obj = dbms.query(query_str)

        if obj[1] == []:
            # error it does not match
            return "invalid username or  password"

        return "Welcome"


        pass
