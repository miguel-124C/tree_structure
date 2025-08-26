from node import Node

class TreeBinary:
    def __init__(self):
        self.raiz=Node()
        self.raiz=None

    def insert(self,ele):
        nuevo=Node()
        nuevo.set_element(ele)

        if self.raiz==None:
            self.raiz=nuevo 
        else:
            aux=self.raiz
            while aux!=None:
                padre=aux
                if(ele<aux.get_element()):
                    aux=aux.get_son_left()
                else:
                    aux=aux.get_son_right()

                if padre.get_element()>nuevo.get_element():
                    padre.left=nuevo
                else:
                    padre.right=nuevo

    def recorrer(self,n):
        if(n!=None):
            self.recorrer(n.get_son_left())
            print(n.get_element())
            self.recorrer(n.get_son_right())