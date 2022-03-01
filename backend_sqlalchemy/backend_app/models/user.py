from backend_sqlalchemy.backend_app.db import db
from backend_sqlalchemy.backend_app.db import app
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship

from passlib.hash import pbkdf2_sha256

# defining a custom hash function to be used for encrypting the password
custom_hash = pbkdf2_sha256.using(salt=bytes(app.secret_key, 'utf-8')).using(rounds=10000).hash

base = automap_base()


class UserModel(base):
    __tablename__ = 'User'

    visits = relationship('Visit', foreign_keys='Visit.uid')

    def encrypt_password(self):
        self.password = custom_hash(self.password)

    def new_password_encrypted(self, password):
        self.password = custom_hash(password)


base.prepare(db.engine, reflect=True)



