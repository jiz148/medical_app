import os

from flask_restful import Resource, reqparse, fields, marshal_with, abort
from itsdangerous import URLSafeTimedSerializer, BadData

from backend_sqlalchemy.backend_app.models.user import UserModel
from backend_sqlalchemy.backend_app.db import db
from backend_sqlalchemy.backend_app.db import app
from backend_sqlalchemy.backend_app.common.send_email import send_email

from backend_sqlalchemy.backend_app.common.contents import FORGET_MY_PASSWORD_SUBJECT, FORGET_MY_PASSWORD_CONTENT

TOKEN_EXP_TIME = 900
TECHNICAL_EMAIL = 'medical_care_555@outlook.com'
EMAIL_PASS = os.getenv('MD_EMAIL_PASS')
SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587

user_register_post_args = reqparse.RequestParser()
user_register_post_args.add_argument("username", type=str, required=True)
user_register_post_args.add_argument("password", type=str, required=True)
user_register_post_args.add_argument("email", type=str, required=True)
user_register_post_args.add_argument("birth_year", type=str, required=True)
user_register_post_args.add_argument("gender", type=str, required=True)
user_register_post_args.add_argument("phone", type=str)

user_login_post_args = reqparse.RequestParser()
user_login_post_args.add_argument("username", type=str, required=True)
user_login_post_args.add_argument("password", type=str, required=True)

user_forget_password_post_args = reqparse.RequestParser()
user_forget_password_post_args.add_argument("email", type=str, required=True)

user_change_password_put_args = reqparse.RequestParser()
user_change_password_put_args.add_argument("token", type=str, required=True)
user_change_password_put_args.add_argument("new_password", type=str, required=True)

resource_field = {
    'uid': fields.Integer,
    'username': fields.String,
}


class UserRegister(Resource):

    def post(self):
        """
        For user Logout
        """
        args = user_register_post_args.parse_args()
        if db.session.query(UserModel).filter(UserModel.username == args['username']).all():
            abort(409, msg='Username already exists')
        if db.session.query(UserModel).filter(UserModel.email == args['email']).all():
            abort(409, msg='Email already exists')
        user = UserModel(username=args['username'],
                         password=args['password'],
                         email=args['email'],
                         birth_year=args['birth_year'],
                         gender=args['gender'],
                         phone=args['phone'])
        db.session.add(user)
        db.session.commit()
        return {"msg": "success"}, 201


class UserLogin(Resource):

    def post(self):
        """
        For User Login
        """
        args = user_login_post_args.parse_args()
        username = args["username"]
        password = args["password"]
        result = db.session.query(UserModel).\
            filter(UserModel.username == username, UserModel.password == password).all()
        if not result:
            abort(401, msg="Invalid username or password")

        return {'msg': 'success'}, 200


class UserForgetPassword(Resource):

    def post(self):
        """
        For user forget password
        """
        args = user_forget_password_post_args.parse_args()
        user_email = args['email']
        s = URLSafeTimedSerializer(app.secret_key, salt='change_my_password')
        token = s.dumps(user_email)
        result = db.session.query(UserModel).filter(UserModel.email == user_email).first()
        if not result:
            abort(401, msg="Email does not exist")

        username = result.username
        email_content = FORGET_MY_PASSWORD_CONTENT.format(user=username, token=token, minutes=int(TOKEN_EXP_TIME / 60))

        try:
            send_email(sender=TECHNICAL_EMAIL,
                       password=EMAIL_PASS,
                       receiver=user_email,
                       subject=FORGET_MY_PASSWORD_SUBJECT,
                       content=email_content,
                       smtp_server=SMTP_SERVER,
                       port=SMTP_PORT)
            return {'msg': 'success'}, 200
        except Exception as e:
            print(e)
            return abort(500, msg='Error when sending email')


class UserChangePassword(Resource):

    def put(self):
        args = user_change_password_put_args.parse_args()
        token = args["token"]
        new_password = args["new_password"]
        s = URLSafeTimedSerializer(app.secret_key, salt='change_my_password')
        email = ''
        try:
            email = s.loads(token, max_age=TOKEN_EXP_TIME)
        except BadData:
            abort(404, msg='Email token is broken')

        user = db.session.query(UserModel).filter(UserModel.email == email).first()
        user.password = new_password
        db.session.commit()
        return {'msg': 'success'}, 200
