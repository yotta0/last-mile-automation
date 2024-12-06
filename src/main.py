from flask import Flask
from src.infra.web_api.routes.user import user_bp

app = Flask(__name__)

app.register_blueprint(user_bp)


if __name__ == '__main__':
    app.run()
