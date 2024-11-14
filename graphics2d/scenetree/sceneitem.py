
import weakref

class SceneItem:
    """
    A SceneItem is any object that can live in the scene tree. 
    """
    
    def __init__(self, **kwargs):
        self.children = []      # Will hold references to all the children
        self.parent = None      # Will hold a weak reference to the parent
        self.tree = None        # Will hold a weak reference to the scene tree

        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = "SceneItem-" + str(id)

    def get_parent():
        if self.parent and self.parent():
            return self.parent()
        else:
            return None

    def get_tree():
        if self.tree and self.tree():
            return self.tree()
        else:
            return None
        
    def enter():
        """
        Callback: Called when the item enters the scene tree
        """
        pass
        
    def exit():
        """
        Callback: Called when the item exists the scene tree
        """
        pass

    def add_child(child):
        if child in self.children:
            raise ValueError("The item {} is already a child of {}".format(child.name, self.name))
        if child.get_parent() != None:
            raise ValueError("The item {} already has parent {} and can't be added as a child of {}".format(child.name, child.get_parent().name, self.name)))
        self.children.append(child)
        child.parent = weakref.ref(self)
        self.child.tree = weakref.ref(tree)
        tree = get_tree()
        if tree:
            tree.notify_enter(child)
        
    def remove_child(child):
        if child.get_parent() != self:
            raise ValueError("The item {} is not a child of {}".format(child.name, self.name))
        tree = get_tree()
        if tree:        
            tree.notify_exit(child)
        self.children.remove(child)
        child.tree = None
        child.parent = None
