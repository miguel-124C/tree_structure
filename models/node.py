
class Node:
    '''Method constructor'''
    def __init__(self):
        self.left: Node=None
        self.right: Node=None
        self.element=0
        self.has_espejo=False
        self.espejo: Node = None

    '''@getters'''
    def get_element(self):
        p=self.element
        return (p)
    def get_son_left(self):
        p=self.left
        return (p)
    def get_son_right(self):
        p=self.right
        return (p)

    '''@setters'''
    def set_element(self,x):
        self.element = x
    def set_son_left(self,x):
        self.left=x
    def set_son_right(self,x):
        self.right=x 