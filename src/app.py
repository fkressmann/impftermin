from flask import Flask


def create_app():
    app = Flask(__name__)
    load_configuration(app)
    register_extensions(app)
    register_blueprints(app)
    return app


def load_configuration(app):
    app.config.from_object('config')

    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{app.config.get('DB_USER')}:{app.config.get('DB_PASSWORD')}@{app.config.get('DB_HOST')}/{app.config.get('DB_NAME')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def register_extensions(app):

    from extensions.db import db
    from extensions.limiter import limiter
    from extensions.migrate import migrate
    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app)
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)


def register_blueprints(app):
    from routes.web import web_bp

    app.register_blueprint(web_bp)

app = create_app()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
