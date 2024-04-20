from flask import Flask
from flask_login import LoginManager

from blueprints.auth import auth as AuthBp
from blueprints.bouquet import bouquet as BouquetBp
from blueprints.profile import profile as ProfileBp
from db import init_db
from helpers import crypto_helper
from models.User import User

app = Flask(__name__)
app.register_blueprint(AuthBp)
app.register_blueprint(BouquetBp)
app.register_blueprint(ProfileBp)
# TODO CHANGE PASSWORD
app.config["SECRET_KEY"] = "VerySr0ngS3cr3tK3y"
app.config["UUID"] = crypto_helper.generate_rnd_string(32)

init_db()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth routes.login"


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.route("/get-uuid")
def get_uuid():
    return app.config["UUID"]


def index():
    return "home.html"


if __name__ == "__main__":
    app.run()
