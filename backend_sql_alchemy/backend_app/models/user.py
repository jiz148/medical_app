from backend_sql_alchemy.backend_app.db import db
from sqlalchemy.ext.automap import automap_base

base = automap_base()
base.prepare(db.engine, reflect=True)


UserModel = base.classes.User
