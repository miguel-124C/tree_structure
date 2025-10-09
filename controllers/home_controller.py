from flask import render_template, Blueprint

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    list_structs = [
        {
            "name": "Tree binary",
            "img": "./../static/images/tree-binary.png",
            "url": "/tree-binary"
        },{
            "name": "Tree M-Vias",
            "img": "/",
            "url": "/treeM-vias",
        },{
            "name": "Grafos",
            "img": "/",
            "url": "/grafos",
        }
    ]

    data = {
        "title": "Mi Página de Inicio",
        "listStructs": list_structs
    }
    return render_template("index.html", data=data)