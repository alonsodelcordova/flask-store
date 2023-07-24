
from functools import wraps
from apps.models.user_model import TokenModel
from flask import request, abort


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        token = request.headers.get('Authorization')
        if not token:
            abort(401, 'Token is required')
        token = token.split(' ')[1]
        token_model = TokenModel.find_by_token(token)
        if not token_model:
            abort(401, 'Invalid token')
            
        request.usuario = token_model.user

        return func(*args, **kwargs)
    return wrapper
