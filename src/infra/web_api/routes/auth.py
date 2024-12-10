from flask import Blueprint, jsonify, request
from dependency_injector.wiring import inject, Provide

from src.interface.web.schemas.user import (UserAuthSchema)
from src.interface.web.controller.auth import AuthController
from src.infra.init.injector import Container


auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('', methods=['POST'])
@inject
def login(auth_controller: AuthController = Provide[Container.auth_controller]):
    user_auth = UserAuthSchema(**request.json)
    return jsonify(auth_controller.login(user_auth))
