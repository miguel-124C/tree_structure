from flask import Blueprint, render_template, request, jsonify, send_file
from models.tree_binary import TreeBinary
import matplotlib.pyplot as plt
import networkx as nx
from io import BytesIO
import base64

# Crear blueprint para las rutas del árbol
tree_bp = Blueprint('tree', __name__)

treeB = TreeBinary()

@tree_bp.route('/')
def index():
    """Pag principal witth visualization tree"""
    return render_template('tree.html')

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

        if order == 'inorden':
            treeB.in_orden(treeB.root)
        elif order == 'preorden':
            treeB.pre_orden(treeB.root)
        elif order == 'postorden':
            treeB.post_orden(treeB.root)
        else:
            return jsonify({'error': 'Orden no valid'}), 400
        
        return jsonify({'elements': 'Aun no se muestra', 'order': order})    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tree_bp.route('/stats')
def get_stats():
    """Get stats the tree"""
    try:
        stats = {
            'height': treeB.height(),
            'amount': treeB.amount(),
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

@tree_bp.route('/tree-image')
def tree_image():
    if treeB.is_empty():
        # Devolver una imagen vacía o mensaje
        return create_empty_tree_image()
    
    # Convertir tu TreeBinary a un grafo de networkx
    G = convert_tree_to_graph(treeB)
    
    # Configurar el gráfico
    plt.figure(figsize=(12, 8))
    
    # Usar layout jerárquico para árboles binarios
    pos = get_tree_layout(G)
    
    # Dibujar el árbol
    nx.draw(G, pos, with_labels=True, node_size=1500, 
            node_color='lightblue', font_size=12, font_weight='bold',
            edge_color='gray', width=2, arrows=False)
    
    plt.title('Árbol Binario - Visualización', fontsize=16, fontweight='bold')
    plt.axis('off')  # Ocultar ejes
    
    # Guardar en buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    buffer.seek(0)
    plt.close()
    
    # Devolver como archivo PNG
    return send_file(buffer, mimetype='image/png', 
                    as_attachment=False, 
                    download_name='arbol_binario.png')

def convert_tree_to_graph(tree_binary):
    """Convierte un TreeBinary a un grafo de networkx"""
    G = nx.DiGraph()  # Grafo dirigido
    
    if tree_binary.is_empty():
        return G
    
    # Función recursiva para agregar nodos y aristas
    def add_nodes_edges(node, parent_value=None):
        if node is None:
            return
        
        node_value = node.get_element()
        
        # Usar el valor como ID del nodo
        G.add_node(node_value, label=str(node_value))
        
        # Agregar arista desde el padre si existe
        if parent_value is not None:
            G.add_edge(parent_value, node_value)
        
        # Recursivamente agregar hijos
        add_nodes_edges(node.get_son_left(), node_value)
        add_nodes_edges(node.get_son_right(), node_value)
    
    # Empezar desde la raíz
    add_nodes_edges(tree_binary.root)
    
    return G

def get_tree_layout(G):
    """Obtiene un layout jerárquico para el árbol sin pygraphviz"""
    if len(G.nodes) == 0:
        return {}
    
    # Encontrar la raíz (nodo sin padres)
    root = None
    for node in G.nodes:
        if G.in_degree(node) == 0:
            root = node
            break
    
    if root is None:
        return nx.spring_layout(G)
    
    try:
        # Intentar usar graphviz_layout si está disponible
        return nx.nx_agraph.graphviz_layout(G, prog='dot', root=root)
    except ImportError:
        # Fallback a layout manual si pygraphviz no está disponible
        return create_manual_tree_layout(G, root)

def create_manual_tree_layout(G, root):
    """Crea un layout jerárquico manual para el árbol"""
    pos = {}
    
    # Calcular la profundidad máxima
    def max_depth(node, depth=0):
        if G.out_degree(node) == 0:
            return depth
        return max(max_depth(child, depth + 1) for child in G.successors(node))
    
    max_depth_val = max_depth(root)
    
    # Asignar posiciones recursivamente
    def assign_positions(node, x, y, level_width):
        pos[node] = (x, -y)  # Invertir y para que crezca hacia abajo
        
        children = list(G.successors(node))
        if not children:
            return x
        
        # Calcular espacio para hijos
        child_count = len(children)
        total_width = level_width * child_count
        start_x = x - total_width / 2 + level_width / 2
        
        current_x = start_x
        for i, child in enumerate(children):
            current_x = assign_positions(child, current_x, y + 1, level_width / 2)
            current_x += level_width
        
        return current_x
    
    # Calcular ancho inicial basado en la profundidad máxima
    initial_width = 2 ** (max_depth_val - 1) if max_depth_val > 0 else 1
    assign_positions(root, 0, 0, initial_width)
    
    return pos

def create_empty_tree_image():
    """Crea una imagen para árbol vacío"""
    plt.figure(figsize=(8, 6))
    plt.text(0.5, 0.5, 'Árbol Vacío', 
             fontsize=20, ha='center', va='center',
             bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.7))
    plt.axis('off')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    
    return send_file(buffer, mimetype='image/png', 
                    download_name='arbol_vacio.png')

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
        'root': serialize_node(treeB.root),
        'stats': {
            'height': treeB.height(),
            'node_count': treeB.amount(),
            'width': treeB.amplitude()
        }
    }
    
    return jsonify(tree_data)