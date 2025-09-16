from flask import render_template, Blueprint

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    data = {
        "title": "Mi Página de Inicio",
        "message": "Bienvenido a mi sitio web!"
    }
    return render_template("index.html", data=data)