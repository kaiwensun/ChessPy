from app import app
from config import settings

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=settings.DEV_PORT_NUMBER)
