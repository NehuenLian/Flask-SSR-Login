from flask import Flask
from config import Config
from extensions import db, csrf, limiter, talisman
from routes.auth import auth_bp
from routes.home import home_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    talisman.init_app(app, content_security_policy=None, force_https=False)

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
