from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from backend.backend_app.resources.users import UsersRegister, UsersLogin, UserForgetPassword

app = Flask(__name__)

# CORS
CORS(app)

api = Api(app)

# users
api.add_resource(UsersRegister, '/users/register', endpoint='users_register')
api.add_resource(UsersLogin, '/users/login', endpoint='users_login')
api.add_resource(UserForgetPassword, '/users/forget_password', endpoint='users_forget_password')


if __name__ == '__main__':
    app.run()
