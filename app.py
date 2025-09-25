from flask import Flask
from controllers.home_controller import home_bp
from controllers.treeBB_controller import tree_bp

def create_app():
    app = Flask(__name__)
    
    # Registrar blueprints
    app.register_blueprint(tree_bp, url_prefix='/tree')
    app.register_blueprint(home_bp, url_prefix='/')
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)