from flask import Blueprint, jsonify, request
from dependency_injector.wiring import inject, Provide

from src.interface.web.schemas.client import ClientCreateSchema, ClientUpdateSchema
from src.interface.web.controller.client import ClientController
from src.interface.web.middleware.auth import auth_required
from src.infra.init.injector import Container

client_bp = Blueprint('client', __name__, url_prefix='/api/v1/clients')

@client_bp.route('', methods=['GET'])
@inject
@auth_required
def get_clients(client_controller: ClientController = Provide[Container.client_controller]):
    """
    Get a list of clients
    ---
    tags:
      - Clients
    summary: Retrieve a paginated list of clients
    description: Retrieve a paginated list of clients with optional page and per_page query parameters.
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
        description: The number of clients to retrieve per page.
    responses:
      200:
        description: A list of clients
        schema:
          type: object
          properties:
            total:
              type: integer
              description: The total number of clients.
            page:
              type: integer
              description: The current page number.
            per_page:
              type: integer
              description: The number of clients per page.
            clients:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: The client ID.
                  name:
                    type: string
                    description: The client name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    return jsonify(client_controller.get_clients(page, per_page))

@client_bp.route('/<int:client_id>', methods=['GET'])
@inject
@auth_required
def get_client(client_id: int, client_controller: ClientController = Provide[Container.client_controller]):
    """
    Get a client by ID
    ---
    tags:
      - Clients
    summary: Retrieve a client by ID
    description: Retrieve a client by ID.
    parameters:
      - name: client_id
        in: path
        type: integer
        required: true
        description: The ID of the client to retrieve.
    responses:
      200:
        description: A client
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The client ID.
            name:
              type: string
              description: The client name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    return jsonify(client_controller.get_client(client_id))

@client_bp.route('', methods=['POST'])
@inject
@auth_required
def create_client(client_controller: ClientController = Provide[Container.client_controller]):
    """
    Create a new client
    ---
    tags:
      - Clients
    summary: Create a new client
    description: Create a new client.
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: ClientCreateSchema
          required:
            - name
          properties:
            name:
              type: string
              description: The client name.
    responses:
      201:
        description: The created client
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The client ID.
            name:
              type: string
              description: The client name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    client = ClientCreateSchema(**request.json)
    return jsonify(client_controller.create_client(client))

@client_bp.route('/<int:client_id>', methods=['PUT'])
@inject
@auth_required
def update_client(client_id: int, client_controller: ClientController = Provide[Container.client_controller]):
    """
    Update a client
    ---
    tags:
      - Clients
    summary: Update a client
    description: Update a client by ID.
    parameters:
      - name: client_id
        in: path
        type: integer
        required: true
        description: The ID of the client to update.
      - name: body
        in: body
        required: true
        schema:
          id: ClientUpdateSchema
          required:
            - name
          properties:
            name:
              type: string
              description: The client name.
    responses:
      200:
        description: The updated client
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The client ID.
            name:
              type: string
              description: The client name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    client = ClientUpdateSchema(**request.json)
    return jsonify(client_controller.update_client(client_id, client))

@client_bp.route('/<int:client_id>', methods=['DELETE'])
@inject
@auth_required
def delete_client(client_id: int, client_controller: ClientController = Provide[Container.client_controller]):
    """
    Delete a client
    ---
    tags:
      - Clients
    summary: Delete a client
    description: Delete a client by ID.
    parameters:
      - name: client_id
        in: path
        type: integer
        required: true
        description: The ID of the client to delete.
    responses:
      200:
        description: The deleted client
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    return jsonify(client_controller.delete_client(client_id))
