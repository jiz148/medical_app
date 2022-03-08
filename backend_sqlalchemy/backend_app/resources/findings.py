from backend_sqlalchemy.backend_app.models.findings import FindingsModel
from backend_sqlalchemy.backend_app.models.visitToFinding import VisitToFindingModel
from backend_sqlalchemy.backend_app.db import db
from backend_sqlalchemy.backend_app.models.user import UserModel
import json
import random
from flask import session
from flask_restful import Resource, reqparse, fields, marshal_with, abort

from backend_sqlalchemy.backend_app.models.visit import VisitModel
visit_to_finding_args = reqparse.RequestParser()
visit_to_finding_args.add_argument("visit_id", type=str, required=True)
visit_to_finding_args.add_argument("Name", type=str, required=True)

#visit_to_finding_args.add_argument("", type=str, required=True)

class Finding(Resource):
    """
    TODO
    """

    def get(self):
        """
        get findings
        """
        args = visit_to_finding_args.parse_args()
        try:
            uid = session['uid']
        except KeyError:
            abort(401, msg="uid in session does not exist")
        visit_id = args['visit_id']
        user_visits = db.session.query(UserModel).filter(UserModel.uid == uid).all().visits
        visit_id_lists = [v.visit_id for v in user_visits]
        if visit_id not in visit_id_lists:
            abort(401, msg="visit does not belong to user")

        findings_from_user = db.session.query(VisitToFindingModel, FindingsModel)\
            .filter(VisitToFindingModel.visit_id == args["visit_id"],
                    FindingsModel.FID == VisitToFindingModel.FID).all()
        answer_name_url = []
        for findings in findings_from_user:
            answer_name_url.append({"answer": findings[0].answer, "Name": findings[1].Name, "URL": findings[1].URL, "FID": findings[1].FID})
        return {"msg": "success", "data": answer_name_url}, 200


    def post(self):
        """
        add findings
        """
        visit_to_finding_args.add_argument("answer", type=str, required=True)
        args = visit_to_finding_args.parse_args()
        try:
            uid = session['uid']
        except KeyError:
            abort(401, msg="uid in session does not exist")

        #findings_from_user = db.session.query(VisitToFindingModel, FindingsModel).filter(VisitToFindingModel.visit_id == args["visit_id"], FindingsModel.FID == VisitToFindingModel.FID).all()
        FID_from_user= db.session.query(FindingsModel).filter(FindingsModel.Name == args["Name"]).first()
        position_in_table = db.session.query(VisitToFindingModel).filter(VisitToFindingModel.visit_id == args["visit_id"]).count()
        visit_to_finding = VisitToFindingModel(position=position_in_table+1, answer=args["answer"], visit_id=args["visit_id"], FID= FID_from_user.FID)
        db.session.add(visit_to_finding)
        db.session.commit()
        return {"msg": "success"}, 200
        answer_name_url = []

        pass

    def delete(self):
        """
        delete findings
        """
        args = visit_to_finding_args.parse_args()
        try:
            uid = session['uid']
        except KeyError:
            abort(401, msg="uid in session does not exist")
        answer_from_user = db.session.query(FindingsModel).filter(FindingsModel.Name == args["Name"]).first()
        visit_id_from_user = args["visit_id"]
        print(answer_from_user.FID, VisitToFindingModel.visit_id)
        db.session.query(VisitToFindingModel).filter(answer_from_user.FID == VisitToFindingModel.FID, visit_id_from_user == VisitToFindingModel.visit_id).delete()
        db.session.commit()
        return {"msg": "deleted!"}, 200
        pass


class NextBestQuestion(Resource):
    """
    TODO
    """

    def get(self):
        all_findings = db.session.query(FindingsModel.FID, FindingsModel.Name, FindingsModel.Title).all()
        findings_hash = {}
        for finding in all_findings:
            findings_hash[finding.Name] = finding.FID
        finding_names = list(findings_hash.keys())

        i = random.randint(0, len(finding_names))
        finding_name = finding_names[i]
        finding = dict()
        finding["Name"] = finding_names[i]
        finding["FID"] = findings_hash[finding_names[i]]

        return {'msg': "success", 'data': finding}

        pass


class TopFindings(Resource):
    """
    TODO
    """

    def get(self):
        all_findings = db.session.query(FindingsModel.FID, FindingsModel.Name, FindingsModel.Title).all()
        findings_hash = {}
        for finding in all_findings:
            findings_hash[finding.Name] = finding.FID
        finding_names = list(findings_hash.keys())

        i = random.randint(0, len(finding_names))
        finding_name = finding_names[i]
        finding = dict()
        finding["Name"] = finding_names[i]
        finding["FID"] = findings_hash[finding_names[i]]

        return {'msg': "success", 'data': finding}


        pass


def get_all_findings():
    """
    Get all findings
    """
    all_findings = db.session.query(FindingsModel.FID, FindingsModel.Name, FindingsModel.Title).all()
    findings_hash = {}
    for finding in all_findings:
        findings_hash[finding.Name] = finding.FID
    return findings_hash



