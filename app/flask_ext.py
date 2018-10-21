from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from redis import StrictRedis

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
redis_client = StrictRedis()
