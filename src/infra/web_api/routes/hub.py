from flask import Blueprint, jsonify, request
from dependency_injector.wiring import inject, Provide

from src.interface.web.schemas.hub import HubCreateSchema, HubUpdateSchema
from src.interface.web.controller.hub import HubController
from src.interface.web.middleware.auth import auth_required
from src.infra.init.injector import Container

hub_bp = Blueprint('hub', __name__, url_prefix='/api/v1/hubs')

@hub_bp.route('', methods=['GET'])
@inject
@auth_required
def get_hubs(hub_controller: HubController = Provide[Container.hub_controller]):
    """
    Get a list of hubs
    ---
    tags:
      - Hubs
    summary: Retrieve a paginated list of hubs
    description: Retrieve a paginated list of hubs with optional page and per_page query parameters.
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
        description: The number of hubs to retrieve per page.
    responses:
      200:
        description: A list of hubs
        schema:
          type: object
          properties:
            total:
              type: integer
              description: The total number of hubs.
            page:
              type: integer
              description: The current page number.
            per_page:
              type: integer
              description: The number of hubs per page.
            hubs:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: The hub ID.
                  name:
                    type: string
                    description: The hub name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    return jsonify(hub_controller.get_hubs(page, per_page))

@hub_bp.route('/<int:hub_id>', methods=['GET'])
@inject
@auth_required
def get_hub(hub_id: int, hub_controller: HubController = Provide[Container.hub_controller]):
    """
    Get a Hub by ID
    ---
    tags:
      - Hubs
    summary: Retrieve a hub by ID
    description: Retrieve a hub by ID.
    parameters:
      - name: hub_id
        in: path
        type: integer
        required: true
        description: The ID of the hub to retrieve.
    responses:
      200:
        description: A hub
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The hub ID.
            name:
              type: string
              description: The hub name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    return jsonify(hub_controller.get_hub(hub_id))

@hub_bp.route('', methods=['POST'])
@inject
@auth_required
def create_hub(hub_controller: HubController = Provide[Container.hub_controller]):
    """
    Create a new hub
    ---
    tags:
      - Hubs
    summary: Create a new hub
    description: Create a new hub.
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: HubCreateSchema
          required:
            - name
          properties:
            name:
              type: string
              description: The hub name.
    responses:
      201:
        description: The created hub
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The hub ID.
            name:
              type: string
              description: The hub name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    hub = HubCreateSchema(**request.json)
    return jsonify(hub_controller.create_hub(hub))

@hub_bp.route('/<int:hub_id>', methods=['PUT'])
@inject
@auth_required
def update_hub(hub_id: int, hub_controller: HubController = Provide[Container.hub_controller]):
    """
    Update a hub
    ---
    tags:
      - Hubs
    summary: Update a hub
    description: Update a hub by ID.
    parameters:
      - name: hub_id
        in: path
        type: integer
        required: true
        description: The ID of the hub to update.
      - name: body
        in: body
        required: true
        schema:
          id: HubUpdateSchema
          required:
            - name
          properties:
            name:
              type: string
              description: The hub name.
    responses:
      200:
        description: The updated hub
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The hub ID.
            name:
              type: string
              description: The hub name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    hub = HubUpdateSchema(**request.json)
    return jsonify(hub_controller.update_hub(hub_id, hub))

@hub_bp.route('/<int:hub_id>', methods=['DELETE'])
@inject
@auth_required
def delete_hub(hub_id: int, hub_controller: HubController = Provide[Container.hub_controller]):
    """
    Delete a hub
    ---
    tags:
      - Hubs
    summary: Delete a hub
    description: Delete a hub by ID.
    parameters:
      - name: hub_id
        in: path
        type: integer
        required: true
        description: The ID of the hub to delete.
    responses:
      200:
        description: The deleted hub
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    return jsonify(hub_controller.delete_hub(hub_id))
