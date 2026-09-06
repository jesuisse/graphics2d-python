from graphics2d.scenetree.notification import Notification

import weakref


class SceneItem:
    """
    A SceneItem is any object that can live in the scene tree.
    """
    
    def __init__(self, **kwargs):
        self.children = []      # Will hold references to all the children
        self.parent = None      # Will hold a weak reference to the parent
        self.tree = None        # Will hold a weak reference to the scene tree
        self._initialized = False # Flag to remember whether on_ready was already called. Managed by Tree.
        self.filtered_events = ()  # Will receive all events

        self.listeners = {}

        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = self.__class__.__name__ + '-' + str(id(self))

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
        Callback: Called when the item enters the scene tree, *before*
        it's children enter the tree.
        """
        pass
        

    def on_child_entered(self, child):
        """
        Callback: Called when a child item enters the scene tree
        """        
        pass

    def on_ready(self):
        """
        Callback: Called when a child item enters the tree for the first
        time, *after* all it's children have run their on_ready's.

        on_ready() runs after on_enter().
        """

    def on_exit(self):
        """
        Callback: Called when the item exists the scene tree
        """
        pass

    def on_update(self, delta_time):
        """
        Callback: Called every frame with the time elapsed since last frame
        """
        pass



    def add_child(self, child):
        """
        Adds a child to this node.
        If we are in the tree, then the whole child's subtree will get on_entered notifications going down the subtree,
        and on_ready coming back up. on_ready only happens the first time a node is added to the tree.
        """
        if child in self.children:
            raise ValueError("The item {} is already a child of {}".format(child.name, self.name))
        if child.get_parent() != None:
            raise ValueError("The item {} already has parent {} and can't be added as a child of {}".format(child.name, child.get_parent().name, self.name))
        self.children.append(child)
        child.parent = weakref.ref(self)
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

    def consume_event(self):
        """
        This marks the currently propagating event as handled so items after this one will not 
        receive the event.
        """
        tree = self.get_tree()
        if tree:
            tree.consume_event()

    def grab_focus(self):
        """
        Make this item the focused one.

        Focused elements are the only ones receiving keyboard input.
        """
        tree = self.get_tree()
        if tree:
            tree.grab_focus(self)
    
    def release_focus(self):
        """
        Release focus.

        Has no effect if this item wasn't focused.
        """
        tree = self.get_tree()
        if tree:
            tree.release_focus(self)

    def emit(self, notification: Notification, *args, **kwargs):
        """
        Emits a signal
        """
        if not notification in self.listeners:
            return
        for listener in self.listeners[notification]:
            #print(self, "emitting", notification, "to", listener, "with args", args)
            listener(self, *args, **kwargs)
        
    
    def listen(self, item: 'SceneItem', notification: Notification, callback):
        """
        Binds a listener callback to a notification from a scene item        
        """
        #TODO: We should probably use weakrefs for the callbacks!
        if not notification in item.listeners:
            item.listeners[notification] = []
        item.listeners[notification].append(callback)
