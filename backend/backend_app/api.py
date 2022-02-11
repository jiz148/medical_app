from flask import Flask
from flask_restful import Api
from backend.backend_app.resources.users import UsersRegister, UsersLogin

app = Flask(__name__)

api = Api(app)

api.add_resource(UsersRegister, '/users/register', endpoint='users_register')
api.add_resource(UsersLogin, '/users/login', endpoint='users_login')


if __name__ == '__main__':
    app.run()
