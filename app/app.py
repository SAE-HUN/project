from flask import Flask

from flask_jwt_extended import JWTManager

from blueprints import user
from models import db
from models.user import User

app = Flask(__name__)
jwt = JWTManager(app)

app.config["SECRET_KEY"] = "1234"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///C:/Users/fjdks/project/app/db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.register_blueprint(user.bp)

db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
