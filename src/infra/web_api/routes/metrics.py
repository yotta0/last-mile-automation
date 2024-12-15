from flask import Blueprint, jsonify, request
from dependency_injector.wiring import inject, Provide

from src.interface.web.controller.attendance import AttendanceController
from src.interface.web.middleware.auth import auth_required
from src.infra.init.injector import Container

metric_bp = Blueprint('metric', __name__, url_prefix='/api/v1/metrics')

@metric_bp.route('/productivity', methods=['GET'])
@inject
@auth_required
def get_productivity_metrics(attendance_controller: AttendanceController = Provide[Container.attendance_controller]):
    """
    Get productivity metrics
    ---
    tags:
      - Attendances
    summary: Retrieve productivity metrics for the attendance system
    description: Retrieve metrics related to productivity, such as the total number of attendances, filtered by optional parameters.
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        description: The page number for pagination.
      - name: per_page
        in: query
        type: integer
        required: false
        description: The number of records per page.
      - name: date_from
        in: query
        type: string
        format: date
        required: false
        description: Filter records from this date (YYYY-MM-DD).
      - name: date_to
        in: query
        type: string
        format: date
        required: false
        description: Filter records up to this date (YYYY-MM-DD).
    responses:
      200:
        description: Productivity metrics
        schema:
          type: object
          properties:
            total_attendances:
              type: integer
              description: The total number of attendances.
            productivity_data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: The ID of the attendance.
                  date:
                    type: string
                    format: date
                    description: The date of the attendance.
                  metric:
                    type: string
                    description: Additional productivity-related data.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    security:
      - Bearer: []
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')

    filters = {
        'date_from': date_from,
        'date_to': date_to
    }

    return jsonify(attendance_controller.get_productivity_metrics(page, per_page, filters, order_by, order_direction))


@metric_bp.route('/sla', methods=['GET'])
@inject
@auth_required
def get_sla_metrics(attendance_controller: AttendanceController = Provide[Container.attendance_controller]):
    """
    Get SLA compliance metrics
    ---
    tags:
      - Attendances
    summary: Retrieve SLA compliance metrics for the attendance system
    description: Retrieve metrics related to SLA compliance, such as the SLA compliance rate and any other related data.
    responses:
      200:
        description: SLA compliance metrics
        schema:
          type: object
          properties:
            sla_compliance_rate:
              type: string
              description: Percentage of attendances meeting SLA criteria.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    security:
      - Bearer: []
    """
    return jsonify(attendance_controller.get_sla_metrics())

@metric_bp.route('/sla/green-angel', methods=['GET'])
@inject
@auth_required
def get_sla_by_green_angels(attendance_controller: AttendanceController = Provide[Container.attendance_controller]):
    """
    Get SLA compliance metrics by Green Angel
    ---
    tags:
      - Attendances
    summary: Retrieve SLA compliance metrics for the attendance system by Green Angel
    description: Retrieve metrics related to SLA compliance by Green Angel, such as the SLA compliance rate and any other related data.
    responses:
      200:
        description: SLA compliance metrics by Green Angel
        schema:
          type: object
          properties:
            green_angel_id:
              type: integer
              description: The Green Angel ID.
            sla_compliance_rate:
              type: string
              description: Percentage of attendances meeting SLA criteria.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    security:
      - Bearer: []
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    green_angel_id = request.args.get('green_angel_id', type=int)
    green_angel_name = request.args.get('green_angel_name')
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')

    filters = {
        'green_angel_id': green_angel_id,
        'green_angel_name': green_angel_name
    }

    return jsonify(attendance_controller.get_sla_metrics_by_green_angels(page, per_page, filters, order_by, order_direction))

@metric_bp.route('/sla/green-angel/<int:green_angel_id>', methods=['GET'])
@inject
@auth_required
def get_sla_by_green_angel(green_angel_id: int, attendance_controller: AttendanceController = Provide[Container.attendance_controller]):
    """
    Get SLA compliance metrics by Green Angel
    ---
    tags:
      - Attendances
    summary: Retrieve SLA compliance metrics for the attendance system by Green Angel
    description: Retrieve metrics related to SLA compliance by Green Angel, such as the SLA compliance rate and any other related data.
    parameters:
      - name: green_angel_id
        in: path
        type: integer
        required: true
        description: The ID of the Green Angel to retrieve metrics for.
    responses:
      200:
        description: SLA compliance metrics by Green Angel
        schema:
          type: object
          properties:
            green_angel_id:
              type: integer
              description: The Green Angel ID.
            sla_compliance_rate:
              type: string
              description: Percentage of attendances meeting SLA criteria.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    security:
      - Bearer: []
    """
    return jsonify(attendance_controller.get_sla_by_green_angel(green_angel_id))


@metric_bp.route('/sla/hub', methods=['GET'])
@inject
@auth_required
def get_sla_by_hubs(attendance_controller: AttendanceController = Provide[Container.attendance_controller]):
    """
    Get SLA compliance metrics by Hub
    ---
    tags:
      - Attendances
    summary: Retrieve SLA compliance metrics for the attendance system by Hub
    description: Retrieve metrics related to SLA compliance by Hub, such as the SLA compliance rate and any other related data.
    responses:
      200:
        description: SLA compliance metrics by Hub
        schema:
          type: object
          properties:
            hub_id:
              type: integer
              description: The Hub ID.
            sla_compliance_rate:
              type: string
              description: Percentage of attendances meeting SLA criteria.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    security:
      - Bearer: []
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    hub_id = request.args.get('hub_id', type=int)
    hub_name = request.args.get('hub_name')
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')

    filters = {
        'hub_id': hub_id,
        'hub_name': hub_name
    }

    return jsonify(attendance_controller.get_sla_metrics_by_hubs(page, per_page, filters, order_by, order_direction))

@metric_bp.route('/sla/hub/<int:hub_id>', methods=['GET'])
@inject
@auth_required
def get_sla_by_hub(hub_id: int, attendance_controller: AttendanceController = Provide[Container.attendance_controller]):
    """
    Get SLA compliance metrics by Hub
    ---
    tags:
      - Attendances
    summary: Retrieve SLA compliance metrics for the attendance system by Hub
    description: Retrieve metrics related to SLA compliance by Hub, such as the SLA compliance rate and any other related data.
    parameters:
      - name: hub_id
        in: path
        type: integer
        required: true
        description: The ID of the Hub to retrieve metrics for.
    responses:
      200:
        description: SLA compliance metrics by Hub
        schema:
          type: object
          properties:
            hub_id:
              type: integer
              description: The Hub ID.
            sla_compliance_rate:
              type: string
              description: Percentage of attendances meeting SLA criteria.
      401:
        description: Unauthorized
      500:
        description: Internal server error
    security:
      - Bearer: []
    """
    return jsonify(attendance_controller.get_sla_by_hub(hub_id))
