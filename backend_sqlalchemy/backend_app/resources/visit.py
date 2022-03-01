import datetime

from flask import session
from flask_restful import Resource, abort
from backend_sqlalchemy.backend_app.models.visit import VisitModel
from backend_sqlalchemy.backend_app.db import db


class Visit(Resource):

    def get(self):
        uid = None
        try:
            uid = session['uid']
        except KeyError:
            abort(401, msg="uid in session does not exist")

        result = db.session.query(VisitModel). \
            filter(VisitModel.uid == uid).all()
        result_json = []
        for r in result:
            result_json.append(r.as_dict())

        return {'msg': 'success', 'result': result_json}, 200


if __name__ == '__main__':
    v = VisitModel()
    # v.visit_id = 2
    v.datetime = datetime.datetime(2022, 6, 11)
    v.note = 'hello2'
    v.uid = 4
    db.session.add(v)
    db.session.commit()


