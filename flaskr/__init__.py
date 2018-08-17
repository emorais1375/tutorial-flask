import os

from flask import Flask
from flask import render_template, url_for

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def dated_url_for(endpoint, **values):
        """dated_url_for."""
        if endpoint == 'static':
            filename = values.get('filename', None)
            if filename:
                file_path = os.path.join(app.root_path, endpoint, filename)
                values['_'] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)

    @app.context_processor
    def override_url_for():
        """override_url_for."""
        return dict(url_for=dated_url_for)

    # a simple page that says hello
    @app.route('/base')
    def base():
        return render_template('base.html')

    @app.route('/laboratorios')
    def laboratorios():
        return render_template('laboratorios.html')

    @app.route('/detalhes')
    def detalhes():
        return render_template('lab_detalhes.html')


    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index1')
    return app
