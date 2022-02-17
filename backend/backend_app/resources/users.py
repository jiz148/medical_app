import os

from flask_restful import Resource
from flask import request

from backend.backend_app.common.db import SqliteDBMS
from backend.backend_app.common.send_email import send_email

from backend.backend_app.resources.path import DATA_FILE_PATH
from backend.backend_app.resources.contents import FORGET_MY_PASSWORD_SUBJECT, FORGET_MY_PASSWORD_CONTENT

TECHNICAL_EMAIL = 'medical_care_555@outlook.com'
EMAIL_PASS = os.getenv('MD_EMAIL_PASS')
SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587


class UsersRegister(Resource):
    def get(self):
        pass

    def post(self):
        dbms = SqliteDBMS(DATA_FILE_PATH)
        data = request.get_json()

        username = data["username"]
        password = data["password"]
        email = data["email"]
        birthday = data["birthday"]
        gender = data["gender"]
        phone = data["phone"]

        query_str_username = "select * from User where username ='"+username+"'"
        obj1 = dbms.query(query_str_username)
        query_str_email = "select * from User where email ='"+email+"'"
        obj2 = dbms.query(query_str_email)

        if obj1[1] != [] or obj2[1] != []:
            # json conversion required
            return {'success': 0, 'msg': 'Username or email already existed'}

        table = 'User'
        col_to_val = {
            # "id": id,
            "username": username,
            "password": password,
            "email": email,
            "birthday": birthday,
            "gender": gender,
            "phone": phone
        }

        dbms.add(table, col_to_val)
        dbms.close()

        return {'success': 1, 'msg': 'Success'}

        pass


class UsersLogin(Resource):
    def get(self):
        pass

    def post(self):

        dbms = SqliteDBMS(DATA_FILE_PATH)
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        query_str = "select * from User where username = '"+username+"' and password ='"+password+"'"
        obj = dbms.query(query_str)

        if obj[1] == []:
            # error it does not match
            return {'success': 0, 'msg': 'Invalid username or password'}

        dbms.close()

        return {'success': 1, 'msg': 'Success'}
        pass


class UserForgetPassword(Resource):

    def get(self):
        dbms = SqliteDBMS(DATA_FILE_PATH)

        data = request.get_json()
        user_email = data['email']

        query_str_email = "select username from User where email ='" + user_email + "'"
        query_result = dbms.query(query_str_email)
        if not query_result[1]:
            return {'success': 0, 'msg': 'Email does not exist'}

        username = query_result[1][0][0]
        email_content = FORGET_MY_PASSWORD_CONTENT.format(username)

        try:
            send_email(sender=TECHNICAL_EMAIL,
                       password=EMAIL_PASS,
                       receiver=user_email,
                       subject=FORGET_MY_PASSWORD_SUBJECT,
                       content=email_content,
                       smtp_server=SMTP_SERVER,
                       port=SMTP_PORT)
            return {'success': 1, 'msg': 'Success'}
        except Exception as e:
            print(e)
            return {'success': 0, 'msg': 'Error when sending email'}


class UserChangePassword(Resource):

    def post(self):

        dbms = SqliteDBMS(DATA_FILE_PATH)
        data = request.get_json()
        username = data["username"]
        new_password = data["password"]

        pass