from datetime import datetime
from flask_login import UserMixin

from my_flask_app.extensions import db, login_manager, bcrypt


# Association table for many-to-many relationship between users and roles
user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return f'<Role {self.name}>'


class Catalog(db.Model):
    __tablename__ = 'catalogs'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Catalog {self.type}:{self.value}>'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    identification = db.Column(db.String(20), unique=True, nullable=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(128))
    city = db.Column(db.String(64))
    birth_date = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    roles = db.relationship('Role', secondary=user_roles, backref='users', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
