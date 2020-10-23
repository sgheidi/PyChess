from anytree import Node, RenderTree

e4 = Node("e4")
d4 = Node("d4")
e5 = Node("e5", parent=e4)
RenderTree()
