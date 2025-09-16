// Configuración de endpoints
const API_BASE = '/tree';

// Elementos DOM
let elements = {
    insertInput: null,
    searchInput: null,
    treeContainer: null,
    traversalResult: null,
    stats: null
};

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    initializeElements();
    attachEventListeners();
    updateStats();
});

function initializeElements() {
    elements = {
        insertInput: document.getElementById('insertElement'),
        searchInput: document.getElementById('searchElement'),
        treeContainer: document.getElementById('treeContainer'),
        traversalResult: document.getElementById('traversalResult'),
        stats: {
            height: document.getElementById('height'),
            amount: document.getElementById('amount'),
            amplitude: document.getElementById('amplitude'),
            isEmpty: document.getElementById('isEmpty')
        }
    };
}

function attachEventListeners() {
    // Event listeners para inputs
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
    const result = await apiCall('/stats');
    
    if (result.success) {
        const { height, amount, amplitude, is_empty } = result.data;
        
        if (elements.stats.height) elements.stats.height.textContent = height;
        if (elements.stats.amount) elements.stats.amount.textContent = amount;
        if (elements.stats.amplitude) elements.stats.amplitude.textContent = amplitude;
        if (elements.stats.isEmpty) elements.stats.isEmpty.textContent = is_empty ? 'Sí' : 'No';
    }
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
        clearTreeVisualization();
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
    
    // Remover después de 5 segundos
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function showTraversalResult(elements, order) {
    if (!elements.traversalResult) return;
    
    const orderNames = {
        'inorden': 'In-Orden',
        'preorden': 'Pre-Orden',
        'postorden': 'Post-Orden'
    };
    
    elements.traversalResult.innerHTML = `
        <div class="traversal-result">
            <h3>Recorrido ${orderNames[order]}:</h3>
            <div class="traversal-path">
                ${elements.join(' → ')}
            </div>
        </div>
    `;
}

function clearTraversalResult() {
    if (elements.traversalResult) {
        elements.traversalResult.innerHTML = '';
    }
}

function updateTreeVisualization() {
    // Mostrar la imagen del árbol
    const timestamp = new Date().getTime(); // Para evitar cache
    const treeImg = document.createElement('img');
    treeImg.src = `/tree/tree-image?t=${timestamp}`;
    treeImg.alt = 'Visualización del árbol binario';
    treeImg.style.maxWidth = '100%';
    treeImg.style.border = '2px solid #ddd';
    treeImg.style.borderRadius = '8px';
    
    // Agregar spinner de carga
    elements.treeContainer.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
            </div>
            <p>Cargando visualización...</p>
        </div>
    `;
    
    // Cuando la imagen se carga, reemplazar el spinner
    treeImg.onload = function() {
        elements.treeContainer.innerHTML = '';
        elements.treeContainer.appendChild(treeImg);
        
        // Agregar botón de actualización
        const refreshBtn = document.createElement('button');
        refreshBtn.className = 'btn btn-secondary mt-2';
        refreshBtn.innerHTML = '🔄 Actualizar Visualización';
        refreshBtn.onclick = updateTreeVisualization;
        elements.treeContainer.appendChild(refreshBtn);
    };
    
    treeImg.onerror = function() {
        elements.treeContainer.innerHTML = `
            <div class="alert alert-error">
                Error al cargar la visualización del árbol
            </div>
            <button class="btn btn-primary mt-2" onclick="updateTreeVisualization()">
                Reintentar
            </button>
        `;
    };
}

function clearTreeVisualization() {
    if (elements.treeContainer) {
        elements.treeContainer.innerHTML = `
            <div class="text-center">
                <p>El árbol está vacío</p>
                <img src="/static/images/empty-tree.png" alt="Árbol vacío" 
                     style="max-width: 200px; opacity: 0.5;">
            </div>
        `;
    }
}

// Exportar funciones para uso global
window.insertElement = insertElement;
window.searchElement = searchElement;
window.traverse = traverse;
window.clearTree = clearTree;
window.updateStats = updateStats;