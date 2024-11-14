from sceneitem import SceneItem

class SceneTree:
    """
    The scene tree holds all objects that participate in the graphics framework.
    """

    def __init__(self, **kwargs):
        self.root = None

    def __del__(self):
        clear_tree()        


    def set_root(root : SceneItem):
        self.root = root
        notify_enter(root)
        
    def clear_tree():
        """
        This removes the tree root item.
        """
        if self.root:
            notify_exit(self.root)
        self.root = None

    
    def notify_enter(item):
        """
        Notifies first the item and then all it's descendants that they have entered the tree
        """
        item.enter()
        for child in item.children:
            notify_enter(child)
    
    def notify_exit(item):
        """
        Notifies first the descendants (depth-first) and then the item that they are about to leave
        the tree
        """
        for child in item.children:
            notify_exit(child)
        item.exit()


