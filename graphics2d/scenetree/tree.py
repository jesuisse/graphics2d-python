import weakref
from graphics2d.scenetree.sceneitem import SceneItem

class SceneTree:
    """
    The scene tree holds all objects that participate in the graphics framework.
    """

    def __init__(self, **kwargs):
        self.root = None
        self.redraw_requests = []
        
    def __del__(self):
        self.clear_tree()        

    def set_root(self, root : SceneItem):
        assert(root.get_tree() is None)
        self.root = root
        root.tree = weakref.ref(self)
        self.notify_enter(root)
        
    def clear_tree(self):
        """
        This removes the tree root item.
        """
        if self.root:
            self.notify_exit(self.root)
        self.root = None

    def has_redraw_requests(self):
        return len(self.redraw_requests) > 0

    def clear_redraw_requests(self):
        self.redraw_requests.clear()

    def request_redraw(self, item):
        """
        Notifies the scene tree that one of it's items needs a redraw.
        """
        self.redraw_requests.append(item)

    
    def notify_enter(self, item):
        """
        Notifies first the item and then all it's descendants that they have entered the tree
        """
        for node in self.depthfirst_preorder(item):
            node.on_enter()
        
    def notify_exit(self, item):
        """
        Notifies first the descendants (depth-first) and then the item that they are about to leave
        the tree
        """
        for node in self.depthfirst_postorder(item):
            node.on_exit()
        
        
    def depthfirst_preorder(self, item: SceneItem = None):
        """
        Generator which yields elements in depth first preorder
        """
        if item is None:
            if self.root is None:
                return
            item = self.root
        yield item
        for child in item.children:
            yield from self.depthfirst_preorder(child)
    
    def depthfirst_postorder(self, item: SceneItem = None):
        """
        Generator which yields elements in depth first postorder
        """
        if item is None:
            if self.root == None:
                return
            item = self.root
        for child in reversed(item.children):
            yield from self.depthfirst_postorder(child)
        yield item

