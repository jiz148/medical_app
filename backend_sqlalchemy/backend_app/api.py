from flask_restful import Api

from backend_sqlalchemy.backend_app.resources.user import \
    UserRegister, \
    UserLogin, \
    UserForgetPassword, \
    UserChangePassword
from backend_sqlalchemy.backend_app.db import create_app


app = create_app()
api = Api(app)

api.add_resource(UserRegister, '/user/register')
api.add_resource(UserLogin, '/user/login')
api.add_resource(UserForgetPassword, '/user/forget_password')
api.add_resource(UserChangePassword, '/user/change_password')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
