from tree_binary import TreeBinary

def main():
   a=TreeBinary()
   a.insert(15)
   a.insert(6)
   a.insert(20)
   a.insert(3)
   a.insert(9)
   a.insert(18)
   a.insert(24)
   a.insert(1)
   a.insert(4)
   a.insert(7)
   a.insert(12)
   a.insert(17)
   a.recorrer(a.raiz)
if __name__=='__main__':
   main()