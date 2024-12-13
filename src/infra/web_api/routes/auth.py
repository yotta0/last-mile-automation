from flask import Blueprint, jsonify, request
from dependency_injector.wiring import inject, Provide

from src.interface.web.schemas.user import UserAuthSchema
from src.interface.web.controller.auth import AuthController
from src.interface.web.middleware.auth import state_auth_required
from src.infra.init.injector import Container

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('', methods=['POST'])
@inject
def login(auth_controller: AuthController = Provide[Container.auth_controller]):
    """
    User login
    ---
    tags:
      - Auth
    summary: User login
    description: Authenticate a user and return a token.
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: UserAuthSchema
          required:
            - email
            - password
          properties:
            email:
              type: string
              description: The user's email.
            password:
              type: string
              description: The user's password.
    responses:
      200:
        description: Authentication successful
        schema:
          type: object
          properties:
            token:
              type: string
              description: The authentication token.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    user_auth = UserAuthSchema(**request.json)
    return jsonify(auth_controller.login(user_auth))

@auth_bp.route('/refresh', methods=['POST'])
@inject
@state_auth_required
def refresh(state: dict, auth_controller: AuthController = Provide[Container.auth_controller]):
    """
    Refresh token
    ---
    tags:
      - Auth
    summary: Refresh authentication token
    description: Refresh the authentication token using the current token.
    responses:
      200:
        description: Token refreshed successfully
        schema:
          type: object
          properties:
            token:
              type: string
              description: The new authentication token.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    return jsonify(auth_controller.refresh(state['sub'], state['id']))
