from flask_restful import Resource, reqparse

from backend_sqlalchemy.backend_app.models.diseases import DiseasesModel
from backend_sqlalchemy.backend_app.db import db
import random

finding_post_args = reqparse.RequestParser()
finding_post_args.add_argument("current_findings", type=dict, action='append', required=True)

g_diseases = {}
g_diseases_freq = {}
g_diseases_prev = {}


class TopDiseases(Resource):
    """
    TODO
    input: current findings
    1. needs input
    2. output: 5 randoms disease
    """

    def post(self):
        args = finding_post_args.parse_args()
        current_findings = args['current_findings']
        #print(current_findings)
        all_diseases_frq = get_all_diseases()
        all_diseases_did = list(all_diseases_frq.keys())
        top_diseases_did = list()
        top_diseases = list()
        for i in range(5):
            c = random.randint(0, len(all_diseases_did) - 1)
            if all_diseases_did[c] not in top_diseases_did:
                top_diseases_did.append(all_diseases_did[c])
                top_diseases.append({'DID': all_diseases_did[c], 'Name': all_diseases_frq[all_diseases_did[c]]})
            else:
                i -= 1
        return {'msg': "success", 'data': top_diseases}


def get_all_diseases():
    """
    Get all diseases
    """
    all_diseases = db.session.query(DiseasesModel.DID, DiseasesModel.Name, DiseasesModel.Frq).all()
    total_freq = sum([d.Frq for d in all_diseases])

    for disease in all_diseases:
        g_diseases[disease.DID] = disease.Name
        g_diseases_freq[disease.DID] = disease.Frq
        g_diseases_prev[disease.DID] = disease.Frq/total_freq
    return g_diseases
