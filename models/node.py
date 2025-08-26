
class Node:
    '''Method constructor'''
    def __init__(self):
        self.left=None
        self.right=None
        self.element=0

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