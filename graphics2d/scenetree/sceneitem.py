
import weakref

class SceneItem:
    """
    A SceneItem is any object that can live in the scene tree. 
    """
    
    def __init__(self, **kwargs):
        self.children = []      # Will hold references to all the children
        self.parent = None      # Will hold a weak reference to the parent
        self.tree = None        # Will hold a weak reference to the scene tree
        self.filtered_events = ()  # Will receive all events

        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = "SceneItem-" + str(id)
        
        if 'filtered_events' in kwargs:
            self.filtered_events = kwargs['filtered_events'] 


    def get_parent(self):
        if self.parent and self.parent():
            return self.parent()
        else:
            return None

    def get_tree(self):
        if self.tree and self.tree():
            return self.tree()
        else:
            return None
        
    def on_enter(self):
        """
        Callback: Called when the item enters the scene tree
        """
        pass
        
    def on_exit(self):
        """
        Callback: Called when the item exists the scene tree
        """
        pass

    def add_child(self, child):
        if child in self.children:
            raise ValueError("The item {} is already a child of {}".format(child.name, self.name))
        if child.get_parent() != None:
            raise ValueError("The item {} already has parent {} and can't be added as a child of {}".format(child.name, child.get_parent().name, self.name))
        self.children.append(child)
        child.parent = weakref.ref(self)
        child.tree = weakref.ref(self.get_tree())
        tree = self.get_tree()
        if tree:
            tree.notify_enter(child)
        
    def remove_child(self, child):
        if child.get_parent() != self:
            raise ValueError("The item {} is not a child of {}".format(child.name, self.name))
        tree = self.get_tree()
        if tree:        
            tree.notify_exit(child)
        self.children.remove(child)
        child.tree = None
        child.parent = None
