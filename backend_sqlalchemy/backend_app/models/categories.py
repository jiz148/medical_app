from backend_sqlalchemy.backend_app.db import db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship

base = automap_base()


class CategoriesModel(base):
    __tablename__ = 'Categories'

    subcategories = relationship('Subcategories', foreign_keys='Subcategories.CID',viewonly=True)


base.prepare(db.engine, reflect=True)

