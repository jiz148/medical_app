from backend_sqlalchemy.backend_app.db import db
from sqlalchemy.ext.automap import automap_base, relationship

base = automap_base()


class DiseasesModel(base):
    __tablename__ = 'Diseases'

    findings = relationship('Findings', secondary='Stats', viewonly=True)


base.prepare(db.engine, reflect=True)

