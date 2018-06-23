from flask import Flask
from config import Config

app = Flask(__name__)


if __name__ == "__main__":
    app.run(debug=True)


def create_app(config_class=Config):
    app = Flask(__name__)

    from app.bokeh import bp as bokeh_bp
    app.register_blueprint(bokeh_bp)

    return app
