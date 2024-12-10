from dependency_injector import containers, providers

from src.infra.database.database import get_db
from src.infra.repository.user import UserRepository
from src.infra.repository.attendance import AttendanceRepository
from src.application.service.user import UserService
from src.application.service.auth import AuthService
from src.application.service.attendance import AttendanceService
from src.interface.web.controller.user import UserController
from src.interface.web.controller.auth import AuthController
from src.interface.web.controller.attendance import AttendanceController


# Container to manage dependencies
class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "src.infra.web_api.routes.user",
        "src.infra.web_api.routes.auth",
        "src.infra.web_api.routes.attendance"
    ])
    db = providers.Resource(get_db)
    user_repository = providers.Factory(UserRepository, db=db)

    attendance_repository = providers.Factory(AttendanceRepository, db=db)


    # Providers for services
    auth_service = providers.Factory(AuthService, user_repository=user_repository)

    user_service = providers.Factory(UserService, user_repository=user_repository, auth_service=auth_service)

    attendance_service = providers.Factory(AttendanceService, attendance_repository=attendance_repository)


    # Providers for controllers
    user_controller = providers.Factory(UserController, user_service=user_service)

    auth_controller = providers.Factory(AuthController, auth_service=auth_service)

    attendance_controller = providers.Factory(AttendanceController, attendance_service=attendance_service)
