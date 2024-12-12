from flask import Blueprint, jsonify, request
from dependency_injector.wiring import inject, Provide

from src.interface.web.schemas.user import (UserCreateSchema, UserUpdateSchema)
from src.interface.web.controller.user import UserController
from src.interface.web.middleware.auth import auth_required
from src.infra.init.injector import Container


user_bp = Blueprint('user', __name__, url_prefix='/api/v1/users')

@user_bp.route('', methods=['GET'])
@inject
@auth_required
def get_users(user_controller: UserController = Provide[Container.user_controller]):
    return jsonify(user_controller.get_users())

@user_bp.route('/<int:user_id>', methods=['GET'])
@inject
@auth_required
def get_user(user_id: int, user_controller: UserController = Provide[Container.user_controller]):
    return jsonify(user_controller.get_user(user_id))

@user_bp.route('', methods=['POST'])
@inject
@auth_required
def create_user(user_controller: UserController = Provide[Container.user_controller]):
    user = UserCreateSchema(**request.json)
    return jsonify(user_controller.create_user(user))


@user_bp.route('/<int:user_id>', methods=['PUT'])
@inject
@auth_required
def update_user(user_id: int, user_controller: UserController = Provide[Container.user_controller]):
    user = UserUpdateSchema(**request.json)
    return jsonify(user_controller.update_user(user_id, user))

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@inject
@auth_required
def delete_user(user_id: int, user_controller: UserController = Provide[Container.user_controller]):
    return jsonify(user_controller.delete_user(user_id))
