from flask_restful import Resource

from backend_sqlalchemy.backend_app.models.diseases import DiseasesModel
from backend_sqlalchemy.backend_app.db import db
import random

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
        all_diseases_frq = get_all_diseases()
        all_diseases_name = list(all_diseases_frq.keys())
        top_diseases = list()
        for i in range(5):
            c = random.randint(0, len(all_diseases_name))
            if all_diseases_name[c] not in top_diseases:
                top_diseases.append(all_diseases_name[c])
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
    return dict(sorted([(g_diseases[i[0]], i[1]) for i in g_diseases_prev.items()], key=lambda x: -x[1]))

