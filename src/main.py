from flask import Flask, jsonify
from flask.json.provider import DefaultJSONProvider

from src.infra.init.injector import Container
from src.infra.web_api.routes.user import user_bp
from src.infra.web_api.routes.auth import auth_bp
from src.infra.web_api.routes.attendance import attendance_bp
from src.domain.exception.domain_exception import DomainException
from src.interface.exception.interface_exception import InterfaceException

from datetime import datetime

container = Container()
app = Flask(__name__)
app.container = container

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%d-%m-%Y %H:%M:%S')
        return super().default(o)

app.json = CustomJSONProvider(app)

@app.errorhandler(DomainException)
def handle_domain_exception(error):
    response = jsonify({
        'code': error.error_code.code,
        'message': error.error_code.message,
        'description': error.error_code.description
    })
    response.status_code = error.error_code.code
    return response

@app.errorhandler(InterfaceException)
def handle_interface_exception(error):
    response = jsonify({
        'code': error.error_code.code,
        'message': error.error_code.message,
        'description': error.error_code.description
    })
    response.status_code = error.error_code.code
    return response

app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(attendance_bp)


if __name__ == '__main__':
    app.run()
