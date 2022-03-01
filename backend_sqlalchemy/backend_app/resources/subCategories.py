from backend_sqlalchemy.backend_app.models.categories import CategoriesModel
from backend_sqlalchemy.backend_app.db import db
import datetime

# needed to make CID a foreign key
if __name__ == '__main__':
    cat = db.session.query(CategoriesModel).first()
    subs = cat.subcategories
    for sub in subs:
        print(sub.SCID)
