from flask_restful import Resource, Api
from flask import request, Blueprint
from apps.models.tareas_model import TareasModel
from apps.utils.autenticate import authenticate
from apps.schemas.tareas_schema import tarea_input_schema, tarea_output_schema, tarea_outputs_schemas

tareas_route = Blueprint(
    'tareas', __name__, 
    url_prefix='/api/v1/tareas')

api = Api(tareas_route)

class TareasResource(Resource):
    method_decorators = [authenticate]

    def get(self):
        tareas = TareasModel.find_by_usuario_id(request.usuario.id)
        return tarea_outputs_schemas.dump(tareas), 200

    def post(self):
        usuario_id = request.usuario.id
        data = tarea_input_schema.load(request.get_json())
        if not data:
            return {'message': 'Invalid data'}, 400
        tarea = TareasModel(**data, usuario_id=usuario_id)
        tarea.save_to_db()
        
        return tarea_output_schema.dump(tarea), 201

class TareaResource(Resource):
    method_decorators = [authenticate]
    def put(self, tarea_id):
        tarea = TareasModel.find_by_usuario_id_and_id(request.usuario.id, tarea_id)
        if not tarea:
            return {'message': 'Tarea not found'}, 404
        data = tarea_input_schema.load(request.get_json())
        if not data:
            return {'message': 'Invalid data'}, 400
        tarea.update_by_id(**data)
        return tarea_output_schema.dump(tarea), 200
    
    def delete(self, tarea_id):
        tarea = TareasModel.find_by_usuario_id_and_id(request.usuario.id, tarea_id)
        if not tarea:
            return {'message': 'Tarea not found'}, 404
        tarea.delete_by_id()
        return {'message': 'Tarea deleted'}, 200

api.add_resource(TareasResource, '/')
api.add_resource(TareaResource, '/<int:tarea_id>')