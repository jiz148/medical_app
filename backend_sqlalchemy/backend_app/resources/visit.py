import datetime

from flask import session
from backend_sqlalchemy.backend_app.models.user import UserModel
from flask_restful import Resource, abort, reqparse
from backend_sqlalchemy.backend_app.models.visit import VisitModel
from backend_sqlalchemy.backend_app.models.visitToFinding import VisitToFindingModel
from backend_sqlalchemy.backend_app.db import db

visit_post_args = reqparse.RequestParser()
visit_post_args.add_argument("note", type=str, required=True)
visit_put_args = reqparse.RequestParser()

visit_put_args.add_argument("visit_id", type=int, required=True)
visit_put_args.add_argument("note", type=str, required=True)
visit_put_args.add_argument("current_findings", type=dict, action='append', required=True)


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
        datetime_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        visit = VisitModel(datetime=datetime_now,
                       note=note,
                       uid=uid)
        user = db.session.query(UserModel).filter(UserModel.uid == uid).first()
        gender = user.gender
        birthyear = user.birth_year
        year_fid, gender_fid = _get_fids_from_year_and_gender(birthyear, gender)

        db.session.add(visit)
        db.session.commit()
        visit_id = visit.visit_id

        visit_to_finding_year = VisitToFindingModel(position=1, answer='yes', visit_id=visit_id, FID=year_fid)
        visit_to_finding_gender = VisitToFindingModel(position=2, answer='yes', visit_id=visit_id, FID=gender_fid)
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

        return {'msg': 'success', 'visit_id': visit_id}
        #return {'msg': 'success', 'result': result_json, 'index': index}

    def put(self):
        args = visit_put_args.parse_args()
        visit_id, note, current_findings = args['visit_id'], args['note'], args['current_findings']
        uid = None
        try:
            uid = session['uid']
        except KeyError:
            abort(401, msg="uid in session does not exist")
        visit = db.session.query(VisitModel).filter(VisitModel.visit_id == visit_id).first()
        if visit.uid != uid:
            abort(401, msg="visit does not belong to user")

        # update note
        visit.note = note
        # clean the old findings
        visit.findings.clear()
        db.session.commit()

        # add new findings
        for i, current_finding in enumerate(current_findings):
            fid = current_finding["FID"]
            answer = current_finding["answer"]
            # add new findings
            v_to_f = VisitToFindingModel(position=i + 1, answer=answer, visit_id=visit_id, FID=fid)
            db.session.add(v_to_f)

        db.session.commit()
        return {'msg': 'success'}


def _get_fids_from_year_and_gender(birthyear, gender):
    cur_year = datetime.datetime.now().year

    if cur_year - birthyear <= 25:
        year_fid = 3735
    elif cur_year - birthyear > 55:
        year_fid = 3736
    else:
        year_fid = 3731

    if gender == 'male':
        gender_fid = 3732
    else:
        gender_fid = 3738

    return year_fid, gender_fid


if __name__ == '__main__':
    v = VisitModel()
    # v.visit_id = 2
    v.datetime = datetime.datetime.now()
    v.note = 'hello2'
    v.uid = 4
    db.session.add(v)
    db.session.commit()
