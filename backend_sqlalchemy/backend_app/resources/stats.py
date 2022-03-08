from backend_sqlalchemy.backend_app.models.diseases import DiseasesModel
from backend_sqlalchemy.backend_app.db import db
from backend_sqlalchemy.backend_app.models.stats import StatsModel


def get_stats():
    """
    Get stats
    """
    all_stats = db.session.query(StatsModel.DID, StatsModel.FID, StatsModel.Sen)
    g_stats = {}
    for stat in all_stats:
        g_stats[(stat.DID, stat.FID)] = stat.Sen
    print(g_stats)



