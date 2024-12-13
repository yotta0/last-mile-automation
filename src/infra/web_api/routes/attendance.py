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
    description: Retrieve a paginated list of attendances with optional page and per_page query parameters.
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
    responses:
      200:
        description: A list of attendances
        schema:
          type: object
          properties:
            total:
              type: integer
              description: The total number of attendances.
            page:
              type: integer
              description: The current page number.
            per_page:
              type: integer
              description: The number of attendances per page.
            attendances:
              type: array
              items:
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
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    return jsonify(attendance_controller.get_attendances(page, per_page))

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
    """
    return jsonify(attendance_controller.delete_attendance(attendance_id))
