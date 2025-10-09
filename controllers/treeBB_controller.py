from flask import Blueprint, render_template, request, jsonify, send_file
from models.tree_binary import TreeBinary

# Crear blueprint para las rutas del árbol
tree_bp = Blueprint('tree', __name__)

treeB = TreeBinary()

@tree_bp.route('/')
def index():
    """Pag principal witth visualization tree"""
    return render_template('treeBB.html')

@tree_bp.route('/insert', methods=['POST'])
def insert_element():
    """Insert element in the tree"""
    try:
        data = request.get_json()
        element = data.get('element')
        
        if element is None:
            return jsonify({'error': 'Element required'}), 400

        # Convertir a número si es posible
        try:
            element = float(element) if '.' in element else int(element)
        except ValueError:
            pass  # Mantener como string si no es número
        
        treeB.insert(element)
        return jsonify({'message': 'Elemento insertado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tree_bp.route('/search', methods=['POST'])
def search_element():
    """Search element in tree"""
    try:
        data = request.get_json()
        element = data.get('element')
        
        if element is None:
            return jsonify({'error': 'Element required'}), 400
        
        # Convertir a número si es posible
        try:
            element = float(element) if '.' in element else int(element)
        except ValueError:
            pass
        
        found = treeB.search(element)
        return jsonify({'found': found, 'element': element})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tree_bp.route('/traverse/<order>')
def traverse_tree(order):
    """Recorrer el árbol en diferentes órdenes"""
    try:
        if treeB.is_empty():
            return jsonify({'elements': [], 'order': order})

        elements = []
        if order == 'inorden':
            elements = treeB.in_orden(treeB.root)
        elif order == 'preorden':
            elements = treeB.pre_orden(treeB.root)
        elif order == 'postorden':
            elements = treeB.post_orden(treeB.root)
        else:
            return jsonify({'error': 'Orden no valid'}), 400

        treeB.elements = []
        return jsonify({'elements': elements, 'order': order})    
    except Exception as elements:
        return jsonify({'error': str(elements)}), 500

@tree_bp.route('/stats')
def get_stats():
    """Get stats the tree"""
    try:
        stats = {
            'height': treeB.height(treeB.root),
            'amount': treeB.amount(treeB.root),
            'amplitude': treeB.amplitude(),
            'is_empty': treeB.is_empty()
        }
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tree_bp.route('/clear', methods=['POST'])
def clear_tree():
    """Clear tree"""
    global treeB
    treeB = TreeBinary()
    return jsonify({'message': 'Ábol reiniciado'})

@tree_bp.route('/tree-data')
def tree_data():
    """Devuelve datos del árbol en formato JSON para visualización"""
    if treeB.is_empty():
        return jsonify({'empty': True})
    
    def serialize_node(node):
        if node is None:
            return None
        
        return {
            'value': node.get_element(),
            'left': serialize_node(node.get_son_left()),
            'right': serialize_node(node.get_son_right()),
            'is_leaf': (node.get_son_left() is None and node.get_son_right() is None)
        }
    
    tree_data = {
        'empty': False,
        'root': serialize_node(treeB.root)
    }
    
    return jsonify(tree_data)

@tree_bp.route('/delete/<element>', methods=['DELETE'])
def delete_node(element):
    try:
        if treeB.is_empty():
            return jsonify({'error': 'Árbol vacio'}), 400
            
        if element is None:
            return jsonify({'error': 'Element required'}), 400

        # Convertir a número si es posible
        try:
            element = float(element) if '.' in element else int(element)
        except ValueError:
            pass  # Mantener como string si no es número
        
        result = treeB.eliminar(element)
        if result :
            return jsonify({'message': 'Elemento se eliminó correctamente'})
        else :
            return jsonify({'message': 'No se eliminó correctamente'})
    except Exception as elements:
        return jsonify({'error': str(elements)}), 500