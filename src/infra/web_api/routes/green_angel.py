from flask import Blueprint, jsonify, request
from dependency_injector.wiring import inject, Provide

from src.interface.web.schemas.green_angel import GreenAngelCreateSchema, GreenAngelUpdateSchema
from src.interface.web.controller.green_angel import GreenAngelController
from src.interface.web.middleware.auth import auth_required
from src.infra.init.injector import Container

green_angel_bp = Blueprint('green_angel', __name__, url_prefix='/api/v1/green-angels')

@green_angel_bp.route('', methods=['GET'])
@inject
@auth_required
def get_green_angels(green_angel_controller: GreenAngelController = Provide[Container.green_angel_controller]):
    """
    Get a list of green angels
    ---
    tags:
      - Green Angels
    summary: Retrieve a paginated list of green angels
    description: Retrieve a paginated list of green angels with optional page and per_page query parameters.
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: The page number to retrieve.
      - name: per_page
        in: query
        type: integer
        required: false
        default: 20
        description: The number of green angels to retrieve per page.
    responses:
      200:
        description: A list of green angels
        schema:
          type: object
          properties:
            total:
              type: integer
              description: The total number of green angels.
            page:
              type: integer
              description: The current page number.
            per_page:
              type: integer
              description: The number of green angels per page.
            green_angels:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: The green angel ID.
                  name:
                    type: string
                    description: The green angel name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    name = request.args.get('name')
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')

    filters = {
        'name': name
    }
    return jsonify(green_angel_controller.get_green_angels(page, per_page, filters, order_by, order_direction))

@green_angel_bp.route('/<int:green_angel_id>', methods=['GET'])
@inject
@auth_required
def get_green_angel(green_angel_id: int, green_angel_controller: GreenAngelController = Provide[Container.green_angel_controller]):
    """
    Get a green angel by ID
    ---
    tags:
      - Green Angels
    summary: Retrieve a green angel by ID
    description: Retrieve a green angel by ID.
    parameters:
      - name: green_angel_id
        in: path
        type: integer
        required: true
        description: The ID of the green angel to retrieve.
    responses:
      200:
        description: A green angel
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The green angel ID.
            name:
              type: string
              description: The green angel name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    return jsonify(green_angel_controller.get_green_angel(green_angel_id))

@green_angel_bp.route('', methods=['POST'])
@inject
@auth_required
def create_green_angel(green_angel_controller: GreenAngelController = Provide[Container.green_angel_controller]):
    """
    Create a new green angel
    ---
    tags:
      - Green Angels
    summary: Create a new green angel
    description: Create a new green angel.
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: GreenAngelCreateSchema
          required:
            - name
          properties:
            name:
              type: string
              description: The green angel name.
    responses:
      201:
        description: The created green angel
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The green angel ID.
            name:
              type: string
              description: The green angel name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    green_angel = GreenAngelCreateSchema(**request.json)
    return jsonify(green_angel_controller.create_green_angel(green_angel))

@green_angel_bp.route('/<int:green_angel_id>', methods=['PUT'])
@inject
@auth_required
def update_green_angel(green_angel_id: int, green_angel_controller: GreenAngelController = Provide[Container.green_angel_controller]):
    """
    Update a green angel
    ---
    tags:
      - Green Angels
    summary: Update a green angel
    description: Update a green angel by ID.
    parameters:
      - name: green_angel_id
        in: path
        type: integer
        required: true
        description: The ID of the green angel to update.
      - name: body
        in: body
        required: true
        schema:
          id: GreenAngelUpdateSchema
          required:
            - name
          properties:
            name:
              type: string
              description: The green angel name.
    responses:
      200:
        description: The updated green angel
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The green angel ID.
            name:
              type: string
              description: The green angel name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    green_angel = GreenAngelUpdateSchema(**request.json)
    return jsonify(green_angel_controller.update_green_angel(green_angel_id, green_angel))

@green_angel_bp.route('/<int:green_angel_id>', methods=['DELETE'])
@inject
@auth_required
def delete_green_angel(green_angel_id: int, green_angel_controller: GreenAngelController = Provide[Container.green_angel_controller]):
    """
    Delete a green angel
    ---
    tags:
      - Green Angels
    summary: Delete a green angel
    description: Delete a green angel by ID.
    parameters:
      - name: green_angel_id
        in: path
        type: integer
        required: true
        description: The ID of the green angel to delete.
    responses:
      200:
        description: The deleted green angel
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    return jsonify(green_angel_controller.delete_green_angel(green_angel_id))
