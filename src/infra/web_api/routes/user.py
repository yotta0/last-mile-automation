from flask import Blueprint

user_bp = Blueprint('user', __name__, url_prefix='/api/v1/users')

@user_bp.route('/')
def get_users():
    return 'Hello World!'

