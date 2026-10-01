from flask import (
    Flask,
    redirect,
    url_for
)

from flask_login import (
    LoginManager,
    current_user
)

from config import Config

from models import (
    db,
    User
)

from routes.auth import auth_bp
from routes.todo import todo_bp
from routes.diary import diary_bp
from routes.schedule import schedule_bp
from routes.dashboard import dashboard_bp


app = Flask(__name__)


app.config.from_object(
    Config
)


db.init_app(app)


login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = (
    "auth.login"
)

login_manager.login_message = (
    "로그인이 필요합니다."
)


@login_manager.user_loader
def load_user(user_id):

    return db.session.get(
        User,
        int(user_id)
    )


app.register_blueprint(
    auth_bp
)

app.register_blueprint(
    todo_bp
)

app.register_blueprint(
    diary_bp
)

app.register_blueprint(
    schedule_bp
)

app.register_blueprint(
    dashboard_bp
)


@app.route("/")
def home():

    if current_user.is_authenticated:

        return redirect(
            url_for(
                "dashboard.dashboard"
            )
        )

    return redirect(
        url_for(
            "auth.login"
        )
    )


with app.app_context():

    db.create_all()


if __name__ == "__main__":

    app.run(
        debug=True
    )