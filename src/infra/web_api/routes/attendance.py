from flask import Blueprint, jsonify, request
from dependency_injector.wiring import inject, Provide

from src.interface.web.schemas.attendance import AttendanceCreateSchema, AttendanceUpdateSchema
from src.interface.web.controller.attendance import AttendanceController
from src.interface.web.middleware.auth import auth_required
from src.infra.init.injector import Container

attendance_bp = Blueprint('attendance', __name__, url_prefix='/api/v1/attendances')

@attendance_bp.route('', methods=['GET'])
@inject
@auth_required
def get_attendances(attendance_controller: AttendanceController = Provide[Container.attendance_controller]):
    """
    Get a list of attendances
    ---
    tags:
      - Attendances
    summary: Retrieve a paginated list of attendances
    description: Retrieve a paginated list of attendances with optional query parameters for filtering and ordering.
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
        description: The number of attendances to retrieve per page.
      - name: client_id
        in: query
        type: integer
        required: false
        description: Filter by client ID.
      - name: green_angel_id
        in: query
        type: integer
        required: false
        description: Filter by green angel ID.
      - name: green_angel_name
        in: query
        type: string
        required: false
        description: Filter by green angel name.
      - name: hub_id
        in: query
        type: integer
        required: false
        description: Filter by hub ID.
      - name: hub_name
        in: query
        type: string
        required: false
        description: Filter by hub name.
      - name: attendance_date
        in: query
        type: string
        required: false
        description: Filter by attendance date.
      - name: limit_date
        in: query
        type: string
        required: false
        description: Filter by limit date.
      - name: order_by
        in: query
        type: string
        required: false
        description: Order by a specific field.
      - name: order_direction
        in: query
        type: string
        required: false
        description: Order direction (asc or desc).
    responses:
      200:
        description: A list of attendances
        schema:
          type: object
          properties:
            size:
              type: integer
              description: The number of attendances in the current page.
            total_pages:
              type: integer
              description: The total number of pages.
            page:
              type: integer
              description: The current page number.
            per_page:
              type: integer
              description: The number of attendances per page.
            items:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: The attendance ID.
                  client_id:
                    type: integer
                    description: The client ID.
                  green_angel_id:
                    type: integer
                    description: The green angel ID.
                  hub_id:
                    type: integer
                    description: The hub ID.
                  attendance_date:
                    type: string
                    description: The attendance date.
                  limit_date:
                    type: string
                    description: The limit date.
                  is_active:
                    type: boolean
                    description: The active status.
                  client:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: The client ID.
                      is_active:
                        type: boolean
                        description: The active status of the client.
                  green_angel:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: The green angel ID.
                      name:
                        type: string
                        description: The green angel name.
                      is_active:
                        type: boolean
                        description: The active status of the green angel.
                  hub:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: The hub ID.
                      name:
                        type: string
                        description: The hub name.
                      is_active:
                        type: boolean
                        description: The active status of the hub.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    security:
      - Bearer: []
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    client_id = request.args.get('client_id', type=int)
    green_angel_id = request.args.get('green_angel_id', type=int)
    green_angel_name = request.args.get('green_angel_name')
    hub_id = request.args.get('hub_id', type=int)
    hub_name = request.args.get('hub_name')
    attendance_date = request.args.get('attendance_date')
    limit_date = request.args.get('limit_date')

    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')

    filters = {
        'client_id': client_id,
        'green_angel_id': green_angel_id,
        'green_angel_name': green_angel_name,
        'hub_id': hub_id,
        'hub_name': hub_name,
        'attendance_date': attendance_date,
        'limit_date': limit_date
    }
    return jsonify(attendance_controller.get_attendances(page, per_page, filters, order_by, order_direction))

@attendance_bp.route('/<int:attendance_id>', methods=['GET'])
@inject
@auth_required
def get_attendance(attendance_id: int, attendance_controller: AttendanceController = Provide[Container.attendance_controller]):
    """
    Get an attendance by ID
    ---
    tags:
      - Attendances
    summary: Retrieve an attendance by ID
    description: Retrieve an attendance by ID.
    parameters:
      - name: attendance_id
        in: path
        type: integer
        required: true
        description: The ID of the attendance to retrieve.
    responses:
      200:
        description: An attendance
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The attendance ID.
            name:
              type: string
              description: The attendance name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    security:
      - Bearer: []
    """
    return jsonify(attendance_controller.get_attendance(attendance_id))

@attendance_bp.route('', methods=['POST'])
@inject
@auth_required
def create_attendance(attendance_controller: AttendanceController = Provide[Container.attendance_controller]):
    """
    Create a new attendance
    ---
    tags:
      - Attendances
    summary: Create a new attendance
    description: Create a new attendance.
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: AttendanceCreateSchema
          required:
            - name
          properties:
            name:
              type: string
              description: The attendance name.
    responses:
      201:
        description: The created attendance
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The attendance ID.
            name:
              type: string
              description: The attendance name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    security:
      - Bearer: []
    """
    attendance = AttendanceCreateSchema(**request.json)
    return jsonify(attendance_controller.create_attendance(attendance))

@attendance_bp.route('/<int:attendance_id>', methods=['PUT'])
@inject
@auth_required
def update_attendance(attendance_id: int, attendance_controller: AttendanceController = Provide[Container.attendance_controller]):
    """
    Update an attendance
    ---
    tags:
      - Attendances
    summary: Update an attendance
    description: Update an attendance by ID.
    parameters:
      - name: attendance_id
        in: path
        type: integer
        required: true
        description: The ID of the attendance to update.
      - name: body
        in: body
        required: true
        schema:
          id: AttendanceUpdateSchema
          required:
            - name
          properties:
            name:
              type: string
              description: The attendance name.
    responses:
      200:
        description: The updated attendance
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The attendance ID.
            name:
              type: string
              description: The attendance name.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    security:
      - Bearer: []
    """
    attendance = AttendanceUpdateSchema(**request.json)
    return jsonify(attendance_controller.update_attendance(attendance_id, attendance))

@attendance_bp.route('/<int:attendance_id>', methods=['DELETE'])
@inject
@auth_required
def delete_attendance(attendance_id: int, attendance_controller: AttendanceController = Provide[Container.attendance_controller]):
    """
    Delete an attendance
    ---
    tags:
      - Attendances
    summary: Delete an attendance
    description: Delete an attendance by ID.
    parameters:
      - name: attendance_id
        in: path
        type: integer
        required: true
        description: The ID of the attendance to delete.
    responses:
      200:
        description: The deleted attendance
      401:
        description: Unauthorized
      500:
        description: Internal server error
    security:
      - Bearer: []
    """
    return jsonify(attendance_controller.delete_attendance(attendance_id))
