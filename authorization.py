from flask import request, jsonify
from functools import wraps

api_username = 'admin'
api_password = 'admin'


def authorized(func):
    @wraps(func)
    def on_decorate(*args, **kwargs):
        username = request.authorization.username
        password = request.authorization.password
        if username == api_username and password == api_password:
            return func(*args, **kwargs)
        return jsonify({'message': 'Authentication failed'}), 403
    return on_decorate


