from backend_sqlalchemy.backend_app.models.visit import VisitModel
from backend_sqlalchemy.backend_app.db import db
import datetime


if __name__ == '__main__':
    v = VisitModel()
    # v.visit_id = 2
    v.datetime = datetime.datetime(2022, 6, 11)
    v.note = 'hello2'
    v.uid = 2
    db.session.add(v)
    db.session.commit()


