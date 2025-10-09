// Configuración de endpoints
const API_BASE = '/tree-binary';

// Elementos DOM
let elements = {
    insertInput: null,
    deleteInput: null,
    searchInput: null,
    traversalResult: null,
    stats: null,
    canvas: null,
};

let ctx;

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    initializeElements();
    attachEventListeners();
    updateStats();
});

function initializeElements() {
    elements = {
        insertInput: document.getElementById('insertElement'),
        deleteInput: document.getElementById('deleteElement'),
        searchInput: document.getElementById('searchElement'),
        traversalResult: document.getElementById('traversalResult'),
        stats: {
            height: document.getElementById('height'),
            amount: document.getElementById('amount'),
            amplitude: document.getElementById('amplitude'),
            isEmpty: document.getElementById('isEmpty')
        },
        canvas: document.getElementById('canvas')
    };

    ctx = elements.canvas.getContext('2d');
}

function attachEventListeners() {
    if (elements.insertInput) {
        elements.insertInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') insertElement();
        });
    }
    
    if (elements.searchInput) {
        elements.searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') searchElement();
        });
    }

    if (elements.deleteInput) {
        elements.deleteInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') deleteElement();
        });
    }
}

// Funciones de API
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Error en la solicitud');
        }
        
        return { success: true, data };
    } catch (error) {
        console.error('API Error:', error);
        showAlert(error.message, 'error');
        return { success: false, error: error.message };
    }
}

// Funciones de operaciones del árbol
async function insertElement() {
    const element = elements.insertInput?.value.trim();
    if (!element) {
        showAlert('Por favor ingrese un elemento', 'error');
        return;
    }
    
    const result = await apiCall('/insert', {
        method: 'POST',
        body: JSON.stringify({ element })
    });
    
    if (result.success) {
        showAlert('Elemento insertado correctamente', 'success');
        elements.insertInput.value = '';
        updateStats();
        updateTreeVisualization();
    }
}

async function deleteElement() {
    const element = elements.deleteInput?.value.trim();
    if (!element) {
        showAlert('Por favor ingrese un elemento', 'error');
        return;
    }

    const result = await apiCall(`/delete/${element}`, {
        method: 'DELETE'
    });

    if (result.success) {
        showAlert(result.data.message, 'success');
        elements.deleteInput.value = '';
        updateStats();
        updateTreeVisualization();
    }
}

async function searchElement() {
    const element = elements.searchInput?.value.trim();
    if (!element) {
        showAlert('Por favor ingrese un elemento', 'error');
        return;
    }
    
    const result = await apiCall('/search', {
        method: 'POST',
        body: JSON.stringify({ element })
    });
    
    if (result.success) {
        const message = result.data.found ? 
            `Elemento "${result.data.element}" encontrado` : 
            `Elemento "${result.data.element}" no encontrado`;
        showAlert(message, result.data.found ? 'success' : 'info');
    }
}

async function traverse(order) {
    const result = await apiCall(`/traverse/${order}`);
    
    if (result.success) {
        showTraversalResult(result.data.elements, order);
    }
}

async function updateStats() {
    const stats = await getStats();

    if (stats) {
        const { height, amount, amplitude, is_empty } = stats;

        if (elements.stats.height) elements.stats.height.textContent = height;
        if (elements.stats.amount) elements.stats.amount.textContent = amount;
        if (elements.stats.amplitude) elements.stats.amplitude.textContent = amplitude;
        if (elements.stats.isEmpty) elements.stats.isEmpty.textContent = is_empty ? 'Sí' : 'No';
    }
}

async function getStats() {
    const result = await apiCall('/stats');
    if (result.success) {
        const { height, amount, amplitude, is_empty } = result.data;
        return { height, amount, amplitude, is_empty };
    }

    return null;
}

async function clearTree() {
    if (!confirm('¿Está seguro de que desea reiniciar el árbol? Se perderán todos los datos.')) {
        return;
    }
    
    const result = await apiCall('/clear', {
        method: 'POST'
    });
    
    if (result.success) {
        showAlert('Árbol reiniciado correctamente', 'success');
        updateStats();
        clearTreeVisualization(true);
        clearTraversalResult();
    }
}

// Funciones de UI
function showAlert(message, type = 'info') {
    // Crear alerta temporal
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        min-width: 300px;
    `;
    
    document.body.appendChild(alertDiv);

    setTimeout(() => {
        alertDiv.remove();
    }, 1000);
}

function showTraversalResult(e, order) {
    console.log(e);
    
    if (!e) return;
    
    const orderNames = {
        'inorden': 'In-Orden',
        'preorden': 'Pre-Orden',
        'postorden': 'Post-Orden'
    };
    
    elements.traversalResult.innerHTML = `
        <div class="traversal-result">
            <h3>Recorrido ${orderNames[order]}:</h3>
            <div class="traversal-path">
                ${e.join(' → ')}
            </div>
        </div>
    `;
}

function clearTraversalResult() {
    if (elements.traversalResult) {
        elements.traversalResult.innerHTML = '';
    }
}

async function updateTreeVisualization() {
    const result = await apiCall('/tree-data');
    if( result.success ) {
        const { empty, root } = result.data;
        if (empty) {
            clearTreeVisualization(true);
            return;
        };

        const x = elements.canvas.width / 2;
        const y = 15;

        clearTreeVisualization();
        const drawLines = (x1, y1, x2, y2)=> {
            ctx.lineWith = 2;
            ctx.fillStyle = 'white';
            ctx.moveTo(x1, y1)
            ctx.lineTo(x2, y2);
            ctx.stroke();
        }

        const drawNodes =({ left, right, value }, x, y, xPrev = null, yPrev = null)=> {
            ctx.beginPath();
            ctx.fillStyle = 'white';
            ctx.arc(x, y, 10, 0, Math.PI * 2);
            ctx.fill();

            ctx.beginPath();
            ctx.font = '8px Arial';
            ctx.fillStyle = 'black';
            ctx.fillText(value, x - 5, y + 5);

            if (left) {
                ctx.beginPath();
                setTimeout(() => {
                    drawNodes(left, x - 20, y + 20, xPrev, yPrev);
                    drawLines(x - 10, y, x - 15, y + 10);
                }, 250);
            }
            if (right) {
                ctx.beginPath();
                setTimeout(() => {
                    drawNodes(right, x + 20, y + 20, xPrev, yPrev);
                    drawLines(x + 10, y, x + 15, y + 10);
                }, 250);
            }
        }

        console.log(root);
        drawNodes(root, x, y);
    }
}

function clearTreeVisualization( treeEmpty = false ) {
    ctx.clearRect(0, 0, elements.canvas.width, elements.canvas.height);
    ctx.fillStyle = '#45abbdff';
    ctx.fillRect(0, 0, elements.canvas.width, elements.canvas.height);

    if( treeEmpty ) {
        ctx.beginPath();
        ctx.font = '16px Arial';
        ctx.fillStyle = 'black';
        ctx.fillText('Árbol vacio', 50, 50);
    }
}