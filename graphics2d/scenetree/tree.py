import weakref
from graphics2d.scenetree.sceneitem import SceneItem
from graphics2d.scenetree.canvasitem import CanvasItem

class SceneTree:
    """
    The scene tree holds all objects that participate in the graphics framework.
    """

    def __init__(self, **kwargs):
        self.root = None
        self.redraw_requests = {}
        self.modalstack = []

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
        self.clear_redraw_requests()

    def make_modal(self, node):
        """ 
        Makes the node modal, e.g. input events will only
        go to that control
        """
        self.modalstack.append(node)
    
    def has_active_modal(self):
        return len(self.modalstack) > 0

    def get_active_modal_node(self):
        if self.has_active_modal():
            return self.modalstack[-1]
        else:
            return None


    def clear_modal(self, node):
        if node in self.modalstack:
            self.modalstack.remove(node)

    def has_redraw_requests(self):
        return len(self.redraw_requests) > 0

    def clear_redraw_requests(self):
        self.redraw_requests.clear()

    def request_redraw(self, item):
        """
        Notifies the scene tree that one of it's items needs a redraw.
        """
        if isinstance(item, CanvasItem):
            self.redraw_requests[item] = True

    def request_redraw_all(self, start_node):
        """
        This requests that the whole tree starting with start_node be redrawn
        """
        for node in self.depthfirst_postorder(start_node):
            if isinstance(node, CanvasItem):
                self.redraw_requests[node] = True

    def notify_enter(self, item):
        """
        Notifies first the item and then all it's descendants that they have entered the tree
        """
        for node in self.depthfirst_preorder(item):
            node.tree = weakref.ref(self)
            node.on_enter()
            self.request_redraw(node)
            parent = node.get_parent()
            if parent:
                parent.on_child_entered(node)


    def notify_exit(self, item):
        """
        Notifies first the descendants (depth-first) and then the item that they are about to leave
        the tree
        """
        for node in self.depthfirst_postorder(item):
            node.on_exit()
            node.tree = None


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

    def canvasitem_roots(self, item: SceneItem = None):
        """
        Generator which yields all the canvasitem roots.

        There can be multiple roots when, for example, the scene
        tree root is not a canvasitem, but has some as children.
        """
        if item is None:
            if self.root == None:
                return
            item = self.root

        if isinstance(item, CanvasItem):
            yield item
            return
        else:
            for child in reversed(item.children):
                yield from self.canvasitem_roots(child)

    def container_roots(self, item: SceneItem = None):
        """
        yields CanvasContainer roots in preorder and CanvasItems
        in reverse depthfirst order.
        """
        if item is None:
            if self.root == None:
                return
            item = self.root
        
        if isinstance(item, CanvasContainer):
            yield item
        else:
            for child in reversed(item.children):
                yield from self.container_roots(child)
            if isinstance(item, CanvasItem):
                yield item
    