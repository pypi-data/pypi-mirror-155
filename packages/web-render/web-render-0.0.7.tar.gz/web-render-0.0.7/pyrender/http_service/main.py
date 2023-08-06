"""
Copyright 2022 Andrey Plugin (9keepa@gmail.com)
Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
"""


def create_app(config):
    import os
    from flask import Flask

    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_object(config)
    from .routing import blueprint_list
    [app.register_blueprint(x) for x in blueprint_list]
    return app


def run_develop(app):
    app.run(port=app.config['FLASK_PORT'],
            host='0.0.0.0', debug=True, use_reloader=False)


def run_production(app):
    from waitress import serve
    serve(app, host='0.0.0.0', port=app.config['FLASK_PORT'])
