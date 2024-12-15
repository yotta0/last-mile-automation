from dependency_injector import containers, providers

from src.infra.database.database import get_db
from src.infra.repository.user import UserRepository
from src.infra.repository.attendance import AttendanceRepository
from src.infra.repository.green_angel import GreenAngelRepository
from src.infra.repository.hub import HubRepository
from src.infra.repository.client import ClientRepository

from src.application.service.user import UserService
from src.application.service.auth import AuthService
from src.application.service.attendance import AttendanceService
from src.application.service.green_angel import GreenAngelService
from src.application.service.hub import HubService
from src.application.service.client import ClientService

from src.interface.web.controller.user import UserController
from src.interface.web.controller.auth import AuthController
from src.interface.web.controller.attendance import AttendanceController
from src.interface.web.controller.green_angel import GreenAngelController
from src.interface.web.controller.hub import HubController
from src.interface.web.controller.client import ClientController


# Container to manage dependencies
class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "src.infra.web_api.routes.user",
        "src.infra.web_api.routes.auth",
        "src.infra.web_api.routes.attendance",
        "src.infra.web_api.routes.green_angel",
        "src.infra.web_api.routes.hub",
        "src.infra.web_api.routes.client",
        "src.infra.web_api.routes.metrics"
    ])
    db = providers.Resource(get_db)
    user_repository = providers.Factory(UserRepository, db=db)

    attendance_repository = providers.Factory(AttendanceRepository, db=db)

    green_angel_repository = providers.Factory(GreenAngelRepository, db=db)

    hub_repository = providers.Factory(HubRepository, db=db)

    client_repository = providers.Factory(ClientRepository, db=db)


    # Providers for services
    auth_service = providers.Factory(AuthService, user_repository=user_repository)

    user_service = providers.Factory(UserService, user_repository=user_repository, auth_service=auth_service)

    attendance_service = providers.Factory(AttendanceService, attendance_repository=attendance_repository)

    green_angel_service = providers.Factory(GreenAngelService, green_angel_repository=green_angel_repository)

    hub_service = providers.Factory(HubService, hub_repository=hub_repository)

    client_service = providers.Factory(ClientService, client_repository=client_repository)


    # Providers for controllers
    user_controller = providers.Factory(UserController, user_service=user_service)

    auth_controller = providers.Factory(AuthController, auth_service=auth_service)

    attendance_controller = providers.Factory(AttendanceController, attendance_service=attendance_service)

    green_angel_controller = providers.Factory(GreenAngelController, green_angel_service=green_angel_service)

    hub_controller = providers.Factory(HubController, hub_service=hub_service)

    client_controller = providers.Factory(ClientController, client_service=client_service)
