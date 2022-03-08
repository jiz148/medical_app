from backend_sqlalchemy.backend_app.db import db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import declarative_base, relationship, backref
from backend_sqlalchemy.backend_app.models.visit import VisitModel
from backend_sqlalchemy.backend_app.models.findings import FindingsModel

from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey, Integer, String

base_dec = declarative_base()
base = automap_base()


class VisitToFindingModel(base):
    __tablename__ = 'VisitToFinding'

    # visit = relationship(VisitModel, backref=backref("VisitToFinding", cascade="all, delete-orphan"))
    # finding = relationship(FindingsModel, backref=backref("VisitToFinding", cascade="all, delete-orphan"))


base.prepare(db.engine, reflect=True)

