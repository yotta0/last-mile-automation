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
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    return jsonify(attendance_controller.get_attendances(page, per_page))

@attendance_bp.route('/<int:attendance_id>', methods=['GET'])
@inject
@auth_required
def get_attendance(attendance_id: int, attendance_controller: AttendanceController = Provide[Container.attendance_controller]):
    return jsonify(attendance_controller.get_attendance(attendance_id))

@attendance_bp.route('', methods=['POST'])
@inject
@auth_required
def create_attendance(attendance_controller: AttendanceController = Provide[Container.attendance_controller]):
    attendance = AttendanceCreateSchema(**request.json)
    return jsonify(attendance_controller.create_attendance(attendance))


@attendance_bp.route('/<int:attendance_id>', methods=['PUT'])
@inject
@auth_required
def update_attendance(attendance_id: int, attendance_controller: AttendanceController = Provide[Container.attendance_controller]):
    attendance = AttendanceUpdateSchema(**request.json)
    return jsonify(attendance_controller.update_attendance(attendance_id, attendance))

@attendance_bp.route('/<int:attendance_id>', methods=['DELETE'])
@inject
@auth_required
def delete_user(attendance_id: int, attendance_controller: AttendanceController = Provide[Container.attendance_controller]):
    return jsonify(attendance_controller.delete_attendance(attendance_id))
