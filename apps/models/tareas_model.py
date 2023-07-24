from apps.database import db
from enum import Enum

class TiposTarea(int,Enum):
    BAJA = 1
    MEDIA = 2
    ALTA = 3

class TareasModel(db.Model):
    __tablename__ = 'tareas_model'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    tarea = db.Column(db.String(256), nullable=False)
    descripcion = db.Column(db.String(256), nullable=False)
    tipo = db.Column(db.Enum(TiposTarea), default=TiposTarea.BAJA, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Tarea {self.tarea}>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_usuario_id(cls, usuario_id):
        return cls.query.filter_by(usuario_id=usuario_id).all()
    
    @classmethod
    def find_by_usuario_id_and_id(cls, usuario_id, _id):
        return cls.query.filter_by(usuario_id=usuario_id, id=_id).first()

    @classmethod
    def delete_by_id(cls, _id):
        cls.query.filter_by(id=_id).delete()
        db.session.commit()

    @classmethod
    def update_by_id(cls, _id, tarea, descripcion):
        cls.query.filter_by(id=_id).update(dict(tarea=tarea, descripcion=descripcion))
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

    @classmethod
    def get_all_like_tarea(cls, tarea):
        return cls.query.filter(cls.tarea.like(f'%{tarea}%')).all()


