from backend_sqlalchemy.backend_app.db import db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import declarative_base, relationship, backref
from backend_sqlalchemy.backend_app.models.visit import VisitModel
from backend_sqlalchemy.backend_app.models.findings import FindingsModel

from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey, Integer, String

base = automap_base()


class FindingsRel(base):
    __tablename__ = 'FindingsRel'


base.prepare(db.engine, reflect=True)
