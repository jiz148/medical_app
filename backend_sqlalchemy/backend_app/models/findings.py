from backend_sqlalchemy.backend_app.common.serializer import json_serial

from backend_sqlalchemy.backend_app.db import db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship

base = automap_base()


class FindingsModel(base):
    __tablename__ = 'Findings'

    visits = relationship('Visit', secondary='VisitToFinding')
    diseases = relationship('Diseases', secondary='Stats',viewonly=True)

    entity_FID2 = relationship('FindingsModel',
                               secondary='FindingsRel',
                               primaryjoin='FindingsModel.FID==FindingsRel.FID1',
                               secondaryjoin='FindingsModel.FID==FindingsRel.FID2',
                               backref='FID2',
                               viewonly=True)

    entity_FID1 = relationship('FindingsModel',
                               secondary='FindingsRel',
                               primaryjoin='FindingsModel.FID==FindingsRel.FID2',
                               secondaryjoin='FindingsModel.FID==FindingsRel.FID1',
                               backref='FID1',
                               viewonly=True)

    def __repr__(self):
        return "<FindingsObject:FID="+str(self.FID)+" Name="+self.Name+">"
    def as_dict(self):
        return {c.name: json_serial(getattr(self, c.name)) for c in self.__table__.columns}


base.prepare(db.engine, reflect=True)





