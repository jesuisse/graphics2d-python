import sys
sys.path.append("..")

from graphics2d.scenetree import SceneTree, SceneItem

t = SceneTree()
root = SceneItem(name="root")
t.set_root(root)

root.add_child(SceneItem(name="first"))
root.add_child(SceneItem(name="second"))

root.children[1].add_child(SceneItem(name="child of second"))

for node in t.depthfirst_postorder(root):
    print(node.name)
    


