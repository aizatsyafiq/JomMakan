import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JSON_AS_ASCII = False

    @staticmethod
    def init_app(app):
        """Hook for config-specific initialization"""
        pass


class DevelopmentConfig(Config):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "development-secret-key-123"
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
    # change default to prod for production
}
