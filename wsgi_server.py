import sys
import logging

from app import app
from config import settings
import importlib

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ['-win', '-linux']:
        logging.error("Usage: {} [-win|-linux]".format(sys.argv[0]))
        quit()
    if sys.argv[1] == '-win':
        waitress = importlib.import_module('waitress')
        waitress.serve(app, host="0.0.0.0", port=int(settings.PORT_NUMBER))
    else:
        gunicorn = importlib.import_module('gunicorn')

        class StandaloneApplication(gunicorn.app.base.BaseApplication):
            def __init__(self, app, **kwargs):
                self.kwargs = kwargs
                self.app = app
                super().__init__()

            def load_config(self):
                for key, value in self.kwargs.items():
                    if key in self.cfg.settings and value is not None:
                        self.cfg.set(key.lower(), value)

            def load(self):
                return self.app

        StandaloneApplication(
            app,
            bind="0.0.0.0:{}".format(settings.PORT_NUMBER),
            workers=4).run()
