from .node import Node

class TreeBinary:

    def __init__(self):
        self.root=None
        self.elements = []
        self.espejos = []

    def insert(self,ele):
        """
            Insert a element in the binary tree
            Parameters: ele -> element to insert
        """
        nuevo=Node()
        nuevo.set_element(ele)

        if self.root == None:
            self.root = nuevo 
        else:
            aux = self.root
            nivel = 0
            while aux != None:
                padre=aux
                nivel = nivel +1
                if(ele < aux.get_element()):
                    aux = aux.get_son_left()
                else:
                    aux = aux.get_son_right()

            print(nivel)
            if padre.get_element() > nuevo.get_element():
                padre.left = nuevo
                self.set_espejo(padre, True, nivel)
            else:
                padre.right = nuevo
                self.set_espejo(padre, False, nivel)

    def set_espejo(self, parent: Node, direction: bool, nivel: int):
        if parent.get_element() == self.root.get_element():
            """True: direccion Der, False: direccion Izq"""
            if direction and self.root.get_son_right():
                self.set_parent_espejos(parent, self.root, direction, nivel)
            else:
                if not direction and self.root.get_son_left():
                    self.set_parent_espejos(parent, self.root, direction, nivel)
        else:
            if not parent.has_espejo: return False

            if direction and parent.espejo.get_son_right():
                self.set_parent_espejos(parent, parent.espejo, not direction, nivel)
            else:
                if not direction and parent.espejo.get_son_left():
                    self.set_parent_espejos(parent, parent.espejo, not direction, nivel)
        

    def set_parent_espejos(self, parent: Node, parent_espejo: Node, dir: bool, nivel: int):
        if dir:
            parent.get_son_right().has_espejo = True
            parent_espejo.get_son_left().has_espejo = True
            parent.get_son_right().espejo = parent_espejo.get_son_left()
            parent_espejo.get_son_left().espejo = parent.get_son_right()
            self.espejos.append(
                [parent_espejo.get_son_left().element, parent.get_son_right().element, nivel]
            )
        else:
            parent_espejo.get_son_right().has_espejo = True
            parent.get_son_left().has_espejo = True
            parent_espejo.get_son_right().espejo = parent.get_son_left()
            parent.get_son_left().espejo = parent_espejo.get_son_right()
            self.espejos.append(
                [parent.get_son_left().element, parent_espejo.get_son_right().element, nivel]
            )

    def get_espejos(self):
        return self.espejos
    
    def del_espejo(self, node):
        index = 0
        for e in self.espejos:
            if node.get_element() == e[0] or node.get_element() == e[1]:
                self.espejos.pop(index)
            index = index+1

    def modify_espejo(self, ele, node):
        index = 0
        for e in self.espejos:
            if ele == e[0]:
                self.espejos[index][0] = node.get_element()
                break
            if ele == e[1]:
                self.espejos[index][1] = node.get_element()
                break
            index = index+1

    def is_empty(self):
        """ Check if the tree is empty """
        return self.root == None

    def is_sheet(self,node):
        """ Check if the node is a sheet """
        return node.get_son_left() == None and node.get_son_right()==None

    def search(self,ele):
        """ Search for an element in the binary tree """
        aux = self.root
        while aux != None:
            if aux.get_element() == ele:
                return True
            elif ele < aux.get_element():
                aux = aux.get_son_left()
            else:
                aux = aux.get_son_right()
        return False

    def height(self, node=None):
        """ Calculate the height of the tree """
        if node is None:
            node = self.root
            return 0
        return 1 + max(self.height(node.get_son_left()), self.height(node.get_son_right()))

    def amount(self, node=None):
        """ Calculate the amount of nodes in the tree """
        if node is None:
            node = self.root
            return 0
        return 1 + self.amount(node.get_son_left()) + self.amount(node.get_son_right())

    def amplitude(self):
        """ Calculate the maximum width of the tree """
        if self.root is None:
            return 0
        queue = [self.root]
        max_width = 0
        while queue:
            width = len(queue)
            max_width = max(max_width, width)
            for _ in range(width):
                node = queue.pop(0)
                if node.get_son_left():
                    queue.append(node.get_son_left())
                if node.get_son_right():
                    queue.append(node.get_son_right())
        return max_width

    """
        2
      1   3
        
        InOrden: 1, 2, 3
    """
    def in_orden(self, node):
        if node is not None:
            self.in_orden(node.get_son_left())
            self.elements.append(node.get_element())
            self.in_orden(node.get_son_right())
        
        return self.elements

    """
        2
      1   3
        PostOrden: 1, 3, 2
    """
    def post_orden(self, node):
        if node is not None:
            self.post_orden(node.get_son_left())
            self.post_orden(node.get_son_right())
            self.elements.append( node.get_element() )
        
        return self.elements

    """
        2
      1   3
        PreOrden: 2, 1, 3
    """
    def pre_orden(self, node):
        if node is not None:
            self.elements.append( node.get_element() )
            self.pre_orden(node.get_son_left())
            self.pre_orden(node.get_son_right())
        
        return self.elements
    
    def _min_value_node(self, node):
        """
        Encuentra el nodo con el valor más pequeño en un subárbol (Sucesor Inmediato).
        """
        current = node
        while current.get_son_left() is not None:
            current = current.get_son_left()
        return current

    def _eliminar_recursivo(self, root, ele):
        """
        Función auxiliar recursiva para la eliminación de nodos.
        """
        # 1. Caso Base: Árbol vacío o elemento no encontrado
        if root is None:
            return root

        # 2. Navegación: Recorre el árbol
        current_element = root.get_element()
        if ele < current_element:
            # Eliminar en subárbol izquierdo
            root.set_son_left(self._eliminar_recursivo(root.get_son_left(), ele))
        elif ele > current_element:
            # Eliminar en subárbol derecho
            root.set_son_right(self._eliminar_recursivo(root.get_son_right(), ele))
        else:
            # ¡El nodo a eliminar es 'root'!

            # 3. Caso 1 & 2: Nodo con 0 o 1 hijo
            if root.get_son_left() is None:
                # Retorna el hijo derecho (puede ser None)
                temp = root.get_son_right()
                if temp:
                    self.del_espejo(temp)
                    self.modify_espejo(root.get_element(), temp)
                if root.has_espejo:
                    self.del_espejo(root)
                return temp
            elif root.get_son_right() is None:
                # Retorna el hijo izquierdo
                temp = root.get_son_left()
                if temp:
                    self.del_espejo(temp)
                    self.modify_espejo(root.get_element(), temp)
                if root.has_espejo:
                    self.del_espejo(root)
                return temp

            # 4. Caso 3: Nodo con 2 hijos
            # Obtener el sucesor inmediato
            temp = self._min_value_node(root.get_son_right())

            # Copiar el contenido del sucesor en este nodo (reemplazo)
            root.set_element(temp.get_element())

            # Eliminar el sucesor del subárbol derecho
            root.set_son_right(self._eliminar_recursivo(root.get_son_right(), temp.get_element()))

        return root
        
    def eliminar(self, ele):
        """
        Método público para eliminar un elemento del árbol.
        """
        if self.root is None:
            return False # Árbol vacío
            
        old_root = self.root
        self.root = self._eliminar_recursivo(self.root, ele)
        
        # Una forma simple de verificar si se eliminó (podría mejorarse)
        return self.root != old_root or self.search(ele) == False