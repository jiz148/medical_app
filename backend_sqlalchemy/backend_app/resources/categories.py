from backend_sqlalchemy.backend_app.models.categories import CategoriesModel
from backend_sqlalchemy.backend_app.db import db

if __name__ == '__main__':
    result = db.session.query(CategoriesModel).limit(5).all()
    for r in result:
        print(r.CID, r.Title)