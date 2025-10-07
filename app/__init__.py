import json
import logging
import os
import time
from typing import Any, Callable, Dict, Optional

from flask import Flask

from .config import config

_FOOD_DATA_CACHE: Optional[Dict[str, Any]] = None
_CACHE_TIMESTAMP: float = 0.0
CACHE_TTL = 300  # 5 minutes


class JomMakanFlask(Flask):
    """Custom Flask app with food data loader."""

    food_data_loader: Callable[[], Dict[str, Any]]


def create_app(config_name: Optional[str] = None) -> JomMakanFlask:
    """Flask application factory."""
    app = JomMakanFlask(__name__)

    if config_name is None:
        config_name = os.environ.get("CONFIG_ENV", "default")

    # Load configuration
    config_class = config.get(config_name, config["default"])
    app.config.from_object(config_class)

    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logging.info("Loaded config: %s (DEBUG=%s)", config_name, app.config["DEBUG"])

    # Production security check
    if config_name == "production" and not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY must be set in production")

    # Register data loader with app context
    def load_food_data() -> Dict[str, Any]:
        """Load food list with time-based caching."""
        global _FOOD_DATA_CACHE, _CACHE_TIMESTAMP
        current_time = time.time()
        if _FOOD_DATA_CACHE is None or (current_time - _CACHE_TIMESTAMP) > CACHE_TTL:
            json_path = os.path.join(app.root_path, "data", "foodlist.json")
            with open(json_path, encoding="utf-8") as f:
                _FOOD_DATA_CACHE = json.load(f)
            _CACHE_TIMESTAMP = current_time
            app.logger.info(f"Food data cache refreshed at {current_time}")

        # Ensure we never return None - this should not happen in practice
        if _FOOD_DATA_CACHE is None:
            raise RuntimeError("Failed to load food data")
        return _FOOD_DATA_CACHE

    app.food_data_loader = load_food_data

    # Register blueprints
    from .routes import main

    app.register_blueprint(main)

    return app
