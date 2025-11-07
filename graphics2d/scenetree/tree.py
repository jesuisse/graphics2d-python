import sys
import weakref
import traceback
from graphics2d.scenetree.sceneitem import SceneItem
from graphics2d.scenetree.canvasitem import CanvasItem, CanvasRectAreaItem
from graphics2d.scenetree.canvascontainer import CanvasContainer
from graphics2d.events import is_focus_event, is_pointer_event

class SceneTree:
    """
    The scene tree holds all objects that participate in the graphics framework.
    """

    def __init__(self, **kwargs):
        self.root = SceneItem(name="root placeholder")
        self.redraw_requests = {}
        self.modalstack = []
        # Stores the currently focused tree item
        self.focused = None

        self.event_consumed = False


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
    
    def grab_focus(self, node):
        print(node.name, "grabbed focus")
        self.focused = node

    def release_focus(self, node):
        if self.focused == node:
            self.focused = None

    def consume_event(self):
        self.event_consumed = True       

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
            self.request_redraw_all(self.root)

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
            

    def request_redraw_all(self, start_node = None):
        """
        This requests that the whole tree starting with start_node be redrawn
        """
        if start_node is None:
            start_node = self.root
        for node in self.depthfirst_postorder(start_node):
            if isinstance(node, CanvasItem):
                self.redraw_requests[node] = True


    def notify_enter(self, item):
        """
        Notifies first the item and then all it's descendants that they have entered the tree.
        
        This takes care of 
           - setting the tree property
           - calling on_enter()
           - requesting a redraw if the item is a CanvasItem
           - recursively handling all children
           - calling on_child_entered() for each child
           - calling on_ready() if this is the first time the item is added to the tree
        """
        item.tree = weakref.ref(self)
        item.on_enter()
        if isinstance(item, CanvasItem):
            self.request_redraw(item)
        for child in item.children:
            self.notify_enter(child)
            item.on_child_entered(child)            
        if not item._initialized:
            item.on_ready()


    def notify_exit(self, item):
        """
        Notifies first the descendants (depth-first) and then the item that they are about to leave
        the tree
        """
        for node in self.depthfirst_postorder(item):
            try:
                node.on_exit()
            except Exception as e:
                # we log exceptions to stderr but otherwise ignore them to allow other exit
                # handlers to run cleanly, as there might be external resources that would be left
                # in an undefined state if on_exit wasn't guaranteed to run. TODO: Maybe add interactive
                # debugger hook later on to allow the developer to look at what's wrong?
                print(f"<'{node.name}'>.on_exit() produced an exception:", file=sys.stderr)
                print(e, file=sys.stderr)
                print(traceback.format_exc())
            finally:
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
    
    def perform_updates(self, dt):
        """
        Call update() on all items in the scene tree
        """
        for item in self.depthfirst_postorder():        
            item.on_update(dt)


    def handle_input(self, event, node):
        """
        Handles input events for the scene tree starting at node
        """

        if is_focus_event(event):
            # focus events are only sent to the currently focused item
            # this is most likely wrong: all on_input callbacks should receive them
            if self.focused:
                self.focused.on_input(event)
                if isinstance(self.focused, CanvasRectAreaItem) and not self.event_consumed:
                    self.focused.on_gui_input(event)
                
                # do not send this event to other items in the tree
                return

        if isinstance(node, CanvasContainer):
            node.on_input(event)
            if self.event_consumed:
                return
            node.on_gui_input(event)        
        else:
            # send event to all the children
            for child in node.children:
                self.handle_input(event, child)
                if self.event_consumed:
                    return

            # send event to node's on_input callback
            if isinstance(node, CanvasItem): 
                node.on_input(event)
                if self.event_consumed:
                    return        
            
            # if event wasn't handled, send it to node's on_gui_input
            if isinstance(node, CanvasRectAreaItem):
                node.on_gui_input(event)

