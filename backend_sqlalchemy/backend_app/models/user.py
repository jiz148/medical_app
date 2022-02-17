from backend_sqlalchemy.backend_app.db import db
from sqlalchemy.ext.automap import automap_base

base = automap_base()
base.prepare(db.engine, reflect=True)


UserModel = base.classes.User
