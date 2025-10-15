import os
from typing import Dict, Optional, Type

from dotenv import load_dotenv
from flask import Flask

load_dotenv()


class Config:
    SECRET_KEY: Optional[str] = os.environ.get("SECRET_KEY")
    JSON_AS_ASCII: bool = False

    @staticmethod
    def init_app(app: Flask) -> None:
        """Hook for config-specific initialization"""
        pass


class DevelopmentConfig(Config):
    SECRET_KEY: str = os.environ.get("SECRET_KEY") or "development-secret-key-123"
    DEBUG: bool = True


class ProductionConfig(Config):
    DEBUG: bool = False
    TESTING: bool = False
    PREFERRED_URL_SCHEME = "https"
    LOG_TO_STDOUT: bool = False
    LOG_LEVEL = "INFO"


config: Dict[str, Type[Config]] = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
    # change default to prod for production
}
