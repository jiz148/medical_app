from collections import defaultdict

from flask_restful import Resource, reqparse

from backend_sqlalchemy.backend_app.models.diseases import DiseasesModel
from backend_sqlalchemy.backend_app.models.stats import StatsModel
from backend_sqlalchemy.backend_app.resources.findings import get_all_findings
from backend_sqlalchemy.backend_app.db import db

finding_post_args = reqparse.RequestParser()
finding_post_args.add_argument("current_findings", type=dict, action='append', required=True)

g_diseases = {}
g_findings_to_diseases = defaultdict(list)

NUM_OF_RETURNED_DISEASES = 5


class TopDiseases(Resource):
    """
    input: current findings
    output: top 5 diseases for the findings
    Uses Naive Bayesian
    """

    def post(self):
        args = finding_post_args.parse_args()
        current_findings = args['current_findings']
        prev = []
        top_diseases = []
        # total_sen = _get_total_sen()
        # for i in range(NUM_OF_RETURNED_DISEASES):
        #     top_disease = _find_next_top_disease(current_findings, prev)
        #     top_diseases.append(top_disease)
        #     prev.append(top_disease)
        top_diseases = get_all_findings()
        return {'msg': "success", 'data': top_diseases}


def _find_next_top_disease(findings, prev):
    return 0


def get_all_stats():
    # print(len(g_findings_to_diseases.get(3731)) if g_findings_to_diseases.get(3731) else 'empty')
    if not g_findings_to_diseases:
        all_refs = db.session.query(StatsModel.DID, StatsModel.FID, StatsModel.Sen).all()
        total_sen = sum([r.Sen for r in all_refs])

        for ref in all_refs:
            g_findings_to_diseases[ref.FID].append({
                'DID': ref.DID,
                'freq': ref.Sen / total_sen
            })
    return g_findings_to_diseases


def get_all_diseases():
    """
    Get all diseases
    """
    if not g_diseases:
        all_diseases = db.session.query(DiseasesModel.DID, DiseasesModel.Name, DiseasesModel.Frq).all()
        total_freq = sum([d.Frq for d in all_diseases])

        for disease in all_diseases:
            g_diseases[disease.DID] = {
                'name': disease.Name,
                'freq': disease.Frq / total_freq
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
