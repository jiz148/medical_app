from backend_sqlalchemy.backend_app.models.diseases import DiseasesModel
from backend_sqlalchemy.backend_app.db import db


def get_all_diseases():
    """
    Get all diseases
    """
    all_diseases = db.session.query(DiseasesModel.DID, DiseasesModel.Name, DiseasesModel.Frq).all()
    total_freq = sum([d.Frq for d in all_diseases])
    g_diseases = {}
    g_diseases_freq = {}
    g_diseases_prev = {}
    for disease in all_diseases:
        g_diseases[disease.DID] = disease.Name
        g_diseases_freq[disease.DID] = disease.Frq
        g_diseases_prev[disease.DID] = disease.Frq/total_freq
    print(g_diseases, g_diseases_freq, g_diseases_prev)
