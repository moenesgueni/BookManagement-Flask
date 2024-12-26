# Controller/user_controller.py
from flask import Blueprint, request, jsonify

from Service.jwt_service import jwt_required
from Service.user_service import UserService

user_bp = Blueprint('user', __name__, url_prefix='/login')

@user_bp.route('/', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    token = UserService.authenticate(username, password)

    if token:
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@user_bp.route('/', methods=['GET'])
@jwt_required
def get_profile():
    return jsonify(request.user), 200




