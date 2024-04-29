from flask import Flask
import os
# from flask_caching import Cache

# cache = Cache(config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 600})

def create_app():
    app = Flask(__name__,
                template_folder=os.path.join(os.getcwd(), 'templates'),
                static_folder=os.path.join(os.getcwd(), 'static'))
    app.secret_key = os.urandom(24)

    # cache.init_app(app)
    
    from .views import main
    app.register_blueprint(main)

    return app