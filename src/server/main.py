from flask import Blueprint, Flask
from flask_cors import CORS

from . import Validator
from .auth import AuthController
from .database import DatabaseProvider
from .stock_market import StockMarketController


class Server:
    """Main application start point."""

    def __init__(self) -> None:
        """Initialize server application along with its endpoints and cors."""
        DatabaseProvider.initialize()
        Validator.initialize()

        self.name: str = __name__
        self.app: Flask = self._create_app()
        self.ctx = self.app.app_context()
        self.ctx.push()

        self.cors: CORS = CORS(
            self.app, origins=["http://localhost:3000", "https://ctb-agh.netlify.app"]
        )
        self._setup_endpoints()

    def _create_app(self) -> Flask:
        """Create Flask server."""
        return Flask(self.name)

    def _setup_endpoints(self) -> None:
        """Create endpoints on the Flask server."""
        self.app.add_url_rule("/", view_func=hello_world_endpoint)

        self.api: Blueprint = Blueprint("api", self.name, url_prefix="/api")
        self.v1: Blueprint = Blueprint("v1", self.name, url_prefix="/v1")
        self.v1.register_blueprint(AuthController.blueprint)
        self.v1.register_blueprint(StockMarketController.blueprint)
        self.api.register_blueprint(self.v1)
        self.app.register_blueprint(self.api)


def hello_world_endpoint() -> str:
    """Root endpoint."""
    return "<p>Hello, World!</p>"


def create_app() -> Flask:
    """Server launch."""
    server = Server()
    return server.app
