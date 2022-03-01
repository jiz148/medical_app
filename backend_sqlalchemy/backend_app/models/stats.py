from backend_sqlalchemy.backend_app.db import db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import declarative_base, relationship, backref
from backend_sqlalchemy.backend_app.models.diseases import DiseasesModel
from backend_sqlalchemy.backend_app.models.findings import FindingsModel

from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey, Integer, String

base_dec = declarative_base()
base = automap_base()


class StatsModel(base):
    __tablename__ = 'Stats'

    disease = relationship(DiseasesModel, backref=backref("Stats", cascade="all, delete-orphan"), viewonly=True)
    finding = relationship(FindingsModel, backref=backref("Stats", cascade="all, delete-orphan"),viewonly=True)


base.prepare(db.engine, reflect=True)
