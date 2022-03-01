from backend_sqlalchemy.backend_app.db import db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship

base = automap_base()


class VisitModel(base):
    __tablename__ = 'Visit'

    findings = relationship('Findings', secondary='VisitToFinding')


base.prepare(db.engine, reflect=True)


