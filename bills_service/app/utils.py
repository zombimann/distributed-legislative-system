# app/utils.py
import jwt
from functools import wraps
from flask import request, jsonify
from app import app

def validate_jwt(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        secret_key = app.config['SECRET_KEY']
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({'message': 'Authorization header missing.'}), 401

        try:
            token_type, encoded_token = auth_header.split()
            if token_type.lower() != 'bearer':
                raise jwt.InvalidTokenError()

            # Decode the JWT and verify its signature
            decoded_jwt = jwt.decode(encoded_token, secret_key, algorithms=['HS256'])
            author_id = request.get_json().get('author_id')

            if not author_id or decoded_jwt.get('sub') != author_id:
                return jsonify({'message': 'Unauthorized to perform this action.'}), 401

            return fn(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired.'}), 401

        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token.'}), 401

    return wrapper
