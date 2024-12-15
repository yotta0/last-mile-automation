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
    """
    Get a list of users
    ---
    tags:
      - Users
    summary: Retrieve a list of users
    description: Retrieve a list of users.
    responses:
      200:
        description: A list of users
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: The user ID.
              name:
                type: string
                description: The user name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    security:
      - Bearer: []
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    name = request.args.get('name')
    email = request.args.get('email')
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')

    filters = {
        'name': name,
        'email': email
    }
    return jsonify(user_controller.get_users(page, per_page, filters, order_by, order_direction))

@user_bp.route('/<int:user_id>', methods=['GET'])
@inject
@auth_required
def get_user(user_id: int, user_controller: UserController = Provide[Container.user_controller]):
    """
    Get a user by ID
    ---
    tags:
      - Users
    summary: Retrieve a user by ID
    description: Retrieve a user by ID.
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The ID of the user to retrieve.
    responses:
      200:
        description: A user
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The user ID.
            name:
              type: string
              description: The user name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    security:
      - Bearer: []
    """
    return jsonify(user_controller.get_user(user_id))

@user_bp.route('', methods=['POST'])
@inject
@auth_required
def create_user(user_controller: UserController = Provide[Container.user_controller]):
    """
    Create a new user
    ---
    tags:
      - Users
    summary: Create a new user
    description: Create a new user.
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: UserCreateSchema
          required:
            - name
          properties:
            name:
              type: string
              description: The user name.
    responses:
      201:
        description: The created user
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The user ID.
            name:
              type: string
              description: The user name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    security:
      - Bearer: []
    """
    user = UserCreateSchema(**request.json)
    return jsonify(user_controller.create_user(user))

@user_bp.route('/<int:user_id>', methods=['PUT'])
@inject
@auth_required
def update_user(user_id: int, user_controller: UserController = Provide[Container.user_controller]):
    """
    Update a user
    ---
    tags:
      - Users
    summary: Update a user
    description: Update a user by ID.
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The ID of the user to update.
      - name: body
        in: body
        required: true
        schema:
          id: UserUpdateSchema
          required:
            - name
          properties:
            name:
              type: string
              description: The user name.
    responses:
      200:
        description: The updated user
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The user ID.
            name:
              type: string
              description: The user name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    security:
      - Bearer: []
    """
    user = UserUpdateSchema(**request.json)
    return jsonify(user_controller.update_user(user_id, user))

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@inject
@auth_required
def delete_user(user_id: int, user_controller: UserController = Provide[Container.user_controller]):
    """
    Delete a user
    ---
    tags:
      - Users
    summary: Delete a user
    description: Delete a user by ID.
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The ID of the user to delete.
    responses:
      200:
        description: The deleted user
      401:
        description: Unauthorized
      500:
        description: Internal server error
    security:
      - Bearer: []
    """
    return jsonify(user_controller.delete_user(user_id))
