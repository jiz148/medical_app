import os

from flask_restful import Resource, reqparse, fields, marshal_with, abort

from backend_sqlalchemy.backend_app.models.user import UserModel
from backend_sqlalchemy.backend_app.db import db
from backend_sqlalchemy.backend_app.common.send_email import send_email

from backend_sqlalchemy.backend_app.common.contents import FORGET_MY_PASSWORD_SUBJECT, FORGET_MY_PASSWORD_CONTENT

TECHNICAL_EMAIL = 'medical_care_555@outlook.com'
EMAIL_PASS = os.getenv('MD_EMAIL_PASS')
SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("username", type=str, required=True)
user_post_args.add_argument("password", type=str, required=True)
user_post_args.add_argument("email", type=str, required=True)
user_post_args.add_argument("birth_year", type=str, required=True)
user_post_args.add_argument("gender", type=str, required=True)
user_post_args.add_argument("phone", type=str)

user_get_args = reqparse.RequestParser()
user_get_args.add_argument("username", type=str, required=True)
user_get_args.add_argument("password", type=str, required=True)

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("email", type=str, required=True)

resource_field = {
    'uid': fields.Integer,
    'username': fields.String,
}


class User(Resource):

    def get(self):
        """
        For User Login
        """
        args = user_get_args.parse_args()
        username = args["username"]
        password = args["password"]
        result = db.session.query(UserModel).\
            filter(UserModel.username == username, UserModel.password == password).all()
        if not result:
            abort(401, msg="Invalid username or password")

        return {'msg': 'success'}, 200

    def post(self):
        """
        For user Logout
        """
        args = user_post_args.parse_args()
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

    def put(self):
        """
        For user forget password
        """
        args = user_put_args.parse_args()
        user_email = args['email']
        result = db.session.query(UserModel).filter(UserModel.email == user_email).first()
        if not result:
            abort(401, msg="Email does not exist")

        username = result.username
        email_content = FORGET_MY_PASSWORD_CONTENT.format(username)

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

