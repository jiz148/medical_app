from flask_restful import Resource

from backend_sqlalchemy.backend_app.models.diseases import DiseasesModel
from backend_sqlalchemy.backend_app.db import db

g_diseases = {}
g_diseases_freq = {}
g_diseases_prev = {}


class TopDiseases(Resource):
    """
    TODO
    """

    def get(self):
        get_top_10_disease = get_all_diseases()
        name_of_dis_stats={}
        k=0
        for i in get_top_10_disease.keys():
            k += 1
            name_of_dis_stats[i] = get_top_10_disease[i]
            if k == 10:
                break
        return {'msg': "success", 'data': name_of_dis_stats}





        pass


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

