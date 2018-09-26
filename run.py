from app import app
from config import settings

if __name__ == "__main__":
    app.run(port=settings.DEV_PORT_NUMBER)