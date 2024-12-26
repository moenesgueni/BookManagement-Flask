# Service/jwt_service.py
import jwt
import datetime
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "your_secret_key"

def generate_jwt(payload):
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token valable 1 heure
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None  # Token expiré
    except jwt.InvalidTokenError:
        return None  # Token invalide

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token missing"}), 401

        # Supprimer "Bearer " si présent
        token = token.replace("Bearer ", "")

        decoded = verify_jwt(token)
        if not decoded:
            return jsonify({"error": "Invalid or expired token"}), 401

        # Ajouter les données décodées dans la requête
        request.user = decoded
        return f(*args, **kwargs)
    return decorated_function
