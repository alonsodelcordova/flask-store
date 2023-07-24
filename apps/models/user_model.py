from apps.database import  db
from enum import Enum
from uuid import uuid4

class TiposUser(int,Enum):
    ADMIN = 1
    USER = 2
    GUEST = 3

class UserModel(db.Model):
    __tablename__ = 'user_model'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    tipo = db.Column(db.Enum(TiposUser), default=TiposUser.USER, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str)-> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def delete_by_id(cls, _id):
        cls.query.filter_by(id=_id).delete()
        db.session.commit()

    @classmethod
    def update_by_id(cls, _id, username, password):
        cls.query.filter_by(id=_id).update(dict(username=username, password=password))
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_all_active(cls):
        return cls.query.filter_by(is_active=True).all()

    @classmethod
    def get_all_inactive(cls):
        return cls.query.filter_by(is_active=False).all()
    

class TokenModel(db.Model):
    __tablename__ = 'token_model'
    usuario_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), primary_key=True)
    token = db.Column(db.String(80), unique=True, nullable=False)

    user = db.relationship('UserModel', backref=db.backref('tokens', lazy=True))

    def __repr__(self):
        return f'<Token {self.token} - {self.usuario_id}>'
    
    @classmethod
    def generate_token(cls, user_id: int)-> "TokenModel":
        token = cls.query.filter_by(usuario_id=user_id).first()
        if token:
            return token
        token = str(uuid4())
        token_model = cls(usuario_id=user_id, token=token)
        db.session.add(token_model)
        db.session.commit()
        return token_model
    
    @classmethod
    def find_by_token(cls, token: str)-> "TokenModel":
        return cls.query.filter_by(token=token).first()
    
    @classmethod
    def delete_by_token(cls, token: str):
        cls.query.filter_by(token=token).delete()
        db.session.commit()

        
        