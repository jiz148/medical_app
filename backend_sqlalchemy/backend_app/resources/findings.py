from backend_sqlalchemy.backend_app.models.findings import FindingsModel
from backend_sqlalchemy.backend_app.models.visitToFinding import VisitToFindingModel
from backend_sqlalchemy.backend_app.db import db
from backend_sqlalchemy.backend_app.models.user import UserModel
import json
import random
from flask import session
from backend_sqlalchemy.backend_app.models.stats import StatsModel
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from backend_sqlalchemy.backend_app.resources.diseases import get_all_stats

from backend_sqlalchemy.backend_app.models.visit import VisitModel
visit_to_finding_get_args = reqparse.RequestParser()
visit_to_finding_get_args.add_argument("visit_id", type=str, required=True)
visit_to_finding_post_args = reqparse.RequestParser()
visit_to_finding_post_args.add_argument("visit_id", type=str, required=True)
visit_to_finding_post_args.add_argument("Name", type=str, required=True)


# visit_to_finding_args.add_argument("", type=str, required=True)

finding_search_get_args = reqparse.RequestParser()
finding_search_get_args.add_argument("keyword", type=str, required=True)
finding_search_get_args.add_argument("current_findings", type=dict, action="append", required=True)

nbq_diseases_get_args = reqparse.RequestParser()
nbq_diseases_get_args.add_argument("top_disease_id", type=int, required=True, location='json')
nbq_diseases_get_args.add_argument("current_findings", type=list, required=True, location='json')

findings_hash = {}
findings_type = {}


class Finding(Resource):
    """
    TODO
    """

    def post(self):
        """
        get findings
        """
        args = visit_to_finding_get_args.parse_args()
        try:
            uid = session['uid']
        except KeyError:
            abort(401, msg="uid in session does not exist")
        visit_id = int(args['visit_id'])
        user = db.session.query(UserModel).filter(UserModel.uid == uid).first()
        user_visits = user.visits
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

    def put(self):
        """
        add findings
        Not needed for now
        """
        visit_to_finding_post_args.add_argument("answer", type=str, required=True)
        args = visit_to_finding_post_args.parse_args()
        try:
            uid = session['uid']
        except KeyError:
            abort(401, msg="uid in session does not exist")

        #findings_from_user = db.session.query(VisitToFindingModel, FindingsModel).filter(VisitToFindingModel.visit_id == args["visit_id"], FindingsModel.FID == VisitToFindingModel.FID).all()
        FID_from_user = db.session.query(FindingsModel).filter(FindingsModel.Name == args["Name"]).first()
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
        # TODO
        '''
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
        '''


class FindingsSearch(Resource):
    """
    TODO
    """

    def post(self):
        """
        try:
            uid = session['uid']
        except KeyError:
            abort(401, msg="uid in session does not exist")

        @return:
        """
        args = finding_search_get_args.parse_args()
        keywords = args['keyword'].split(' ')
        cur_findings = []
        for i in args["current_findings"]:
            if i and i["checked"]:
                ob = {}
                ob['Name'] = i["Name"]
                ob['FID'] = i['FID']
                cur_findings.append(ob)
        # print(args["current_findings"])
        new_string = ''
        for keyword in keywords:
            new_string += '%'+keyword+'%'
        findings = db.session.query(FindingsModel.FID, FindingsModel.Name, FindingsModel.URL).filter(FindingsModel.Name.like(new_string)).all()
        search_result = list()
        for finding in findings:
            f = {}
            f['FID'] = finding.FID
            f['Name'] = finding.Name
            f['URL'] = finding.URL
            if f in cur_findings:  # args['current_findings']:
                continue
            search_result.append(f)
        max_length = 25
        search_result = search_result[:max_length]
        return {'msg': "success", 'data': search_result}


class NextBestQuestion(Resource):
    """
    TODO
    The get method needs a input
    input - top diseases and selected findings list, output- next best finding(random for now)
    """

    def post(self):
        '''try:
            uid = session['uid']
        except KeyError:
            abort(401, msg="uid in session does not exist")'''
        global findings_type
        args = nbq_diseases_get_args.parse_args()
        disease_id = args["top_disease_id"]
        cur_findings = []
        for i in args["current_findings"]:
            if i:#if i and i["checked"]:
                cur_findings.append(i["FID"])
        if not findings_type:
            all_findings = db.session.query(FindingsModel.FID,
                                            FindingsModel.Type).all()
            for finding in all_findings:
                findings_type[finding.FID] = finding.Type
        # finding_ids = list(findings_hash.keys())
        '''while 1:
            i = random.randint(0, len(finding_names))
            finding_name = finding_names[i]
            if findings_hash[finding_name] in cur_findings:
                continue
            else:
                break
        finding = dict()
        finding["Name"] = finding_names[i]
        finding["FID"] = findings_hash[finding_names[i]]'''
        all_stats = get_all_stats()
        disease_stats = []
        for stat in all_stats:
            if stat[0] == disease_id and stat[1] not in cur_findings:

                disease_stats.append(stat)
        nbq_fid = 0
        nbq_value = -1
        for stat in disease_stats:
            if stat[2] > nbq_value and findings_type[stat[1]] <= int(len(cur_findings)) / 6 + 1:
                if _is_age(stat[1]):
                    for fid in cur_findings:
                        if _is_age(fid):
                            continue
                if _is_gender(stat[1]):
                    for fid in cur_findings:
                        if _is_gender(fid):
                            continue
                nbq_value = stat[2]
                nbq_fid = stat[1]
        finding_details = db.session.query(FindingsModel.FID, FindingsModel.Name, FindingsModel.URL).filter(
            FindingsModel.FID == nbq_fid).first()

        nbq_finding = dict()
        nbq_finding['FID'] = finding_details['FID']
        nbq_finding['Name'] = finding_details['Name']
        nbq_finding['URL'] = finding_details['URL']
        return {'msg': "success", 'data': nbq_finding}


class TopFindings(Resource):
    """
    Not Needed
    """

    def get(self):
        all_findings = db.session.query(FindingsModel.FID, FindingsModel.Name, FindingsModel.Title).all()
        findings_hash = get_all_findings()
        finding_names = list(findings_hash.keys())
        top_findings = {}
        selected_i = []
        print(finding_names)
        j = 0
        while j < 10:
            i = random.randint(0, len(finding_names))
            print(i)
            if i in selected_i:
                continue
            selected_i.append(i)
            top_findings[finding_names[i]] = findings_hash[finding_names[i]]
            j += 1

        return {'msg': "success", 'data': top_findings}


def get_all_findings():
    """
    Get all findings
    """
    if not findings_hash:
        all_findings = db.session.query(FindingsModel.FID, FindingsModel.Name, FindingsModel.Title).all()
        total_findings = len(all_findings)
        for finding in all_findings:
            findings_hash[finding.FID] = {
                "name": finding.Name,
                "freq": 1 / total_findings
            }
    return findings_hash


def get_all_stats():
    all_stats = []
    if not all_stats:
        all_stats_query = db.session.query(StatsModel.DID, StatsModel.FID, StatsModel.Sen).all()
        for stat in all_stats_query:
            all_stats.append((stat.DID, stat.FID, stat.Sen))
    return all_stats


def _is_age(fid):
    return True if fid in [3731, 3735, 3736] else False


def _is_gender(fid):
    return True if fid in [3732, 3738] else False
