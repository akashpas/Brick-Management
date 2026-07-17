import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///instance/app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_PROTECTION = "strong"
    WTF_CSRF_TIME_LIMIT = None
    SECURITY_ALLOW_ADVANCES = os.getenv("ALLOW_ADVANCES", "0") == "1"
    # For file exports
    EXPORT_DIR = os.path.join(os.getcwd(), "exports")
    os.makedirs(EXPORT_DIR, exist_ok=True)

class DevelopmentConfig(Config):
    pass

class ProductionConfig(Config):
    pass

def get_config():
    env = os.getenv("FLASK_ENV", "development").lower()
    if env == "production":
        return ProductionConfig
    return DevelopmentConfig
