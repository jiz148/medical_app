import datetime

from flask import session
from backend_sqlalchemy.backend_app.models.user import UserModel
from flask_restful import Resource, abort, reqparse
from backend_sqlalchemy.backend_app.models.visit import VisitModel
from backend_sqlalchemy.backend_app.models.findings import FindingsModel
from backend_sqlalchemy.backend_app.models.visitToFinding import VisitToFindingModel
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
        # TODO
        datetime_now = datetime.datetime.now()
        visit = VisitModel(datetime=datetime_now,
                       note=note,
                       uid=uid)
        user = db.session.query(UserModel).filter(UserModel.uid == uid).first()
        gender = user.gender
        birthyear = user.birth_year
        curyear = datetime.datetime.now().year
        
        visit_id = visit.visit_id
        # TODO
        if curyear - birthyear <= 25:
            year_fid = 3735
            #year_finding = db.session.query(FindingsModel).filter(FindingsModel.FID == 3735).first()
        elif curyear - birthyear > 55:
            year_fid = 3736
            #year_finding = db.session.query(FindingsModel).filter(FindingsModel.FID == 3736).first()
        else:
            year_fid = 3731
            #year_finding = db.session.query(FindingsModel).filter(FindingsModel.FID == 3731).first()

        if gender == 'male':
            gender_fid = 3732
            #gender_finding = db.session.query(FindingsModel).filter(FindingsModel.FID == 3732).first()
        else:
            gender_fid = 3738
            #gender_finding = db.session.query(FindingsModel).filter(FindingsModel.FID == 3738).first()
        
        db.session.add(visit)
        db.session.commit()
        visit_to_finding_year = VisitToFindingModel(position=1, answer='yes', visit_id=visit.visit_id, FID= year_fid)
        visit_to_finding_gender = VisitToFindingModel(position=2, answer='yes', visit_id=visit.visit_id, FID= gender_fid)
        db.session.add(visit_to_finding_year)
        db.session.add(visit_to_finding_gender)
        db.session.commit()

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

    def put(self):
        """
        TODO
        """
        pass


if __name__ == '__main__':
    v = VisitModel()
    # v.visit_id = 2
    v.datetime = datetime.datetime.now()
    v.note = 'hello2'
    v.uid = 4
    db.session.add(v)
    db.session.commit()
