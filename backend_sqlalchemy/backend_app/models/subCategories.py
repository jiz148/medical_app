from backend_sqlalchemy.backend_app.db import db
from sqlalchemy.ext.automap import automap_base

base = automap_base()


class SubCategories(base):
    __tablename__ = 'Subcategories'


base.prepare(db.engine, reflect=True)

