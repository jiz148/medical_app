import flask
from flask import request
from flask_restful import Api

from backend_sqlalchemy.backend_app.resources.user import \
    UserRegister, \
    UserLogin, \
    UserForgetPassword, \
    UserChangePassword, \
    UserData, \
    UserLogout, \
    UserDisclaimer, \
    UserProfile
from backend_sqlalchemy.backend_app.resources.findings import \
    Finding, \
    NextBestQuestion, \
    TopFindings, \
    FindingsSearch
from backend_sqlalchemy.backend_app.resources.diseases import \
    TopDiseases
from backend_sqlalchemy.backend_app.resources.visit import Visit
from backend_sqlalchemy.backend_app.db import create_app


app = create_app()
api = Api(app)

api.add_resource(UserRegister, '/user/register')
api.add_resource(UserLogin, '/user/login')
api.add_resource(UserForgetPassword, '/user/forget_password')
api.add_resource(UserChangePassword, '/user/change_password')
api.add_resource(UserData, '/user/sessiondata')
api.add_resource(UserLogout, '/user/logout')
api.add_resource(UserDisclaimer, '/disclaimer')
api.add_resource(Visit, '/visit')
api.add_resource(Finding, '/finding')
api.add_resource(FindingsSearch, '/finding/finding_search')
api.add_resource(NextBestQuestion, '/finding/nbq')
api.add_resource(TopFindings, '/finding/top_findings')
api.add_resource(TopDiseases, '/disease/top_diseases')
api.add_resource(UserProfile, '/user/profile')


@app.route('/newpass', methods=['GET'])
def change_password():
    token = request.args.get('token')
    return flask.render_template('change_password.html', token=token)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
