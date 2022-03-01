import datetime

from flask import session
from flask_restful import Resource, abort, reqparse
from backend_sqlalchemy.backend_app.models.visit import VisitModel
from backend_sqlalchemy.backend_app.db import db

visit_post_args = reqparse.RequestParser()
visit_post_args.add_argument("note", type=str, required=True)


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

    def post(self):
        args = visit_post_args.parse_args()
        note = args["note"]
        uid = None
        try:
            uid = session['uid']
        except KeyError:
            abort(401, msg="uid in session does not exist")
        datetime_now = datetime.datetime.now()
        visit = VisitModel(datetime=datetime_now,
                       note=note,
                       uid=uid)
        db.session.add(visit)
        db.session.commit()
        visit_id = visit.visit_id

        # return the whole list of visit again
        result = db.session.query(VisitModel). \
            filter(VisitModel.uid == uid).all()
        result_json = []
        for r in result:
            result_json.append(r.as_dict())
        
        # return added index
        index = 0
        for i in range(len(result_json)):
            if result_json[i]['visit_id'] == visit_id:
                index = i

        return {'msg': 'success', 'result': result_json, 'index': index}


if __name__ == '__main__':
    v = VisitModel()
    # v.visit_id = 2
    v.datetime = datetime.datetime.now()
    v.note = 'hello2'
    v.uid = 4
    db.session.add(v)
    db.session.commit()
