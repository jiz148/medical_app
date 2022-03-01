from backend_sqlalchemy.backend_app.db import db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship

from backend_sqlalchemy.backend_app.common.serializer import json_serial

base = automap_base()


class VisitModel(base):
    __tablename__ = 'Visit'

    findings = relationship('Findings', secondary='VisitToFinding')

    def as_dict(self):
        return {c.name: json_serial(getattr(self, c.name)) for c in self.__table__.columns}


base.prepare(db.engine, reflect=True)


