# app.py
from flask import Flask

from auth import auth
from config import FLASK_SECRET_KEY

app = Flask(__name__)
app.config["SECRET_KEY"] = FLASK_SECRET_KEY

app.register_blueprint(auth)

if __name__ == "__main__":
    app.run(debug=True)