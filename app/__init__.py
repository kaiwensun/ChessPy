from flask import Flask

from app.home.views import bp as home_bp

app = Flask(__name__)
app.register_blueprint(home_bp, url_prefix='/home')


app.run(debug=True)
