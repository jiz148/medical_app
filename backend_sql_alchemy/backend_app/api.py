from flask_restful import Api

from backend_sql_alchemy.backend_app.resources.user import User
from backend_sql_alchemy.backend_app.db import create_app


app = create_app()
api = Api(app)

api.add_resource(User, '/user')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
