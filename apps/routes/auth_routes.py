from flask_restful import Resource, Api
from flask import request, Blueprint
from apps.models.user_model import UserModel, TokenModel
from apps.schemas.auth_schemas import login_input_schema, login_output_schema

auth_route = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

api = Api(auth_route)


class AuthRegisterResource(Resource):
    def post(self):
        data = login_input_schema.load(request.get_json())
        if not data:
            return {'message': 'Invalid data'}, 400
        if UserModel.find_by_username(data['username']):
            return {'message': 'User already exists'}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User created'}, 201

class AuthLoginResource(Resource):
    
    def post(self):
        data = login_input_schema.load(request.get_json())
        if not data:
            return {'message': 'Invalid credentials'}, 401
        
        user = UserModel.find_by_username(data['username'])
        
        if user and user.password == data['password']:
            token = TokenModel.generate_token(user.id)
            user.token = token.token
            return login_output_schema.dump(user), 200
        return {'message': 'Invalid credentials'}, 401

    
class AuthLogoutResource(Resource):

    def post(self):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Invalid token'}, 401
        token = token.split(' ')[1]
        token_model = TokenModel.find_by_token(token)
        if not token_model:
            return {'message': 'Invalid token'}, 401
        TokenModel.delete_by_token(token)
            
        return {'message': 'Logout'}, 200


api.add_resource(AuthLoginResource, '/login')
api.add_resource(AuthLogoutResource, '/logout')
api.add_resource(AuthRegisterResource, '/register')

