from . import db
from flask_login import UserMixin
from .liked import Likes

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String, nullable=False, unique=False)
    _surname = db.Column(db.String, nullable=False, unique=False)
    _email = db.Column(db.String, nullable=False, unique=True)
    _password = db.Column(db.String, nullable=False, unique=False)
    _like = db.relationship("Likes", backref='user', lazy=True)

    def __init__(self, name, surname, email, password):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password

    def __eq__(self, value) -> bool:
        if isinstance(value, User):
            return self.email == value.email and self.password == value.password
        elif isinstance(value, str):
            return self.email == value
        else:
            return False

    def __repr__(self) -> str:
        return f'''
                    "name": {self.name},
                    "surname": {self.surname},
                    "email": {self.email},
                    "password": {self.password}
                '''

################################################################

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if value is None:
            self._name = value
            return
        if len(value) < 3:
            raise Exception({"error": "Invalid name"})
        self._name = value

    @property
    def surname(self):
        return self._surname
        
    @surname.setter
    def surname(self, value):
        if value is None:
            self._surname = value
            return
        if len(value) < 3:
            raise Exception({"error": "Invalid surname"})
        self._surname = value

    @property
    def password(self):
        return self._password
        
    @password.setter
    def password(self, value): 
        if value is None:
            self._password = value
            return
        if len(value) < 9:
            raise Exception({"error": "Invalid password"})
        self._password = value

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if value is None:
            self._email = value
            return
        if User.query.filter(getattr(User, '_email') == value).first():
            raise Exception({"error": "Invalid email"})
        self._email = value

################################################################