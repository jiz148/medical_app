from collections import defaultdict

from flask_restful import Resource, reqparse

from backend_sqlalchemy.backend_app.models.diseases import DiseasesModel
from backend_sqlalchemy.backend_app.models.stats import StatsModel
from backend_sqlalchemy.backend_app.resources.findings import get_all_findings
from backend_sqlalchemy.backend_app.db import db

finding_post_args = reqparse.RequestParser()
finding_post_args.add_argument("current_findings", type=dict, action='append', required=True)

g_diseases = {}
g_findings_to_diseases = {}

NUM_OF_RETURNED_DISEASES = 20


class TopDiseases(Resource):
    """
    input: current findings
    output: top 5 diseases for the findings
    Uses Naive Bayesian
    """

    def post(self):
        args = finding_post_args.parse_args()
        # current_findings = args['current_findings']
        current_findings = []  # args['current_findings']
        print(args["current_findings"])
        for i in args["current_findings"]:
            if i and i["checked"]:
                current_findings.append(i)
        all_diseases, all_stats, i = get_all_diseases(), get_all_stats(), 0
        disease_results = []
        for key in all_diseases.keys():
            # firstly get the prob. of disease
            cond_p = all_diseases[key]['freq']
            # multiply by all conditional prob of findings given diseases
            for finding in current_findings:
                fid, answer = finding['FID'], finding['answer']
                f_to_d_freq = all_stats[fid].get(key) if all_stats[fid].get(key) else 0
                if answer != 'unknown':
                    if answer == 'yes':
                        cond_p *= f_to_d_freq / all_diseases[key]['freq']
                    else:
                        cond_p *= 1 - f_to_d_freq / all_diseases[key]['freq']
            disease_results.append({
                "DID": key,
                "Name": all_diseases[key]['name'],
                "cond_p": cond_p,
                "URL": all_diseases[key]['URL']
            })
        disease_results = sorted(disease_results, key=lambda d: d['cond_p'], reverse=True)
        return {'msg': "success", 'data': disease_results[:NUM_OF_RETURNED_DISEASES]}


def get_all_stats():
    # print(len(g_findings_to_diseases.get(3731)) if g_findings_to_diseases.get(3731) else 'empty')
    if not g_findings_to_diseases:
        all_refs = db.session.query(StatsModel.DID, StatsModel.FID, StatsModel.Sen).all()
        # total_sen = sum([r.Sen for r in all_refs])

        for ref in all_refs:
            if not g_findings_to_diseases.get(ref.FID):
                g_findings_to_diseases[ref.FID] = {}
            g_findings_to_diseases[ref.FID][ref.DID] = ref.Sen
    return g_findings_to_diseases


def get_all_diseases():
    """
    Get all diseases
    """
    if not g_diseases:
        all_diseases = db.session.query(DiseasesModel.DID, DiseasesModel.Name, DiseasesModel.Frq, DiseasesModel.URL).all()
        # total_freq = sum([d.Frq for d in all_diseases])

        for disease in all_diseases:
            g_diseases[disease.DID] = {
                'name': disease.Name,
                'freq': disease.Frq,
                'URL': disease.URL
            }
    return g_diseases


if __name__ == "__main__":
    # import time
    # tic = time.perf_counter()
    # total_rel = db.session.query(func.sum(StatsModel.Sen)).first()[0]
    # toc = time.perf_counter()
    # print(f"got result in {toc - tic:0.4f} seconds")
    # print(total_rel)
    #
    # tic = time.perf_counter()
    # total = db.session.query(StatsModel).all()
    # total_sen = sum([r.Sen for r in total])
    # toc = time.perf_counter()
    # print(f"got result in {toc - tic:0.4f} seconds")
    # print(total_sen)
    print(get_all_diseases())
    print(get_all_stats())
