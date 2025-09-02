from node import Node

class TreeBinary:
    def __init__(self):
        self.root=None

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
            while aux != None:
                padre=aux
                if(ele < aux.get_element()):
                    aux = aux.get_son_left()
                else:
                    aux = aux.get_son_right()

            if padre.get_element() > nuevo.get_element():
                padre.left = nuevo
            else:
                padre.right = nuevo

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
            print(node.get_element())
            self.in_orden(node.get_son_right())

    """
        2
      1   3
        PostOrden: 1, 3, 2
    """
    def post_orden(self, node):
        if node is not None:
            self.post_orden(node.get_son_left())
            self.post_orden(node.get_son_right())
            print(node.get_element())

    """
        2
      1   3
        PreOrden: 2, 1, 3
    """
    def pre_orden(self, node):
        if node is not None:
            print(node.get_element())
            self.pre_orden(node.get_son_left())
            self.pre_orden(node.get_son_right())