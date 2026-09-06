

class Theme():
    """
    A theme stores a collection of properties such as 
    font names, font sizes and other style information 
    for a given class.

    It also has a mechanism to look up a property in a 
    parent theme if the property isn't available, making
    it possible to override parent theme values.

    There are base themes for each class. So, if you create
    a new CanvasItem-derived class, you can add default 
    properties for this class to the parent class theme, and
    all classes derived from *your* class will pick up your
    default values if they are not overriden in the 
    derived classes.

    See test_themes.py to see how we use this system.
    
    """


    def __init__(self, match_class, parent=None):
        self._parent = parent
        self._match_class = match_class
        self._children = {}
        if self._parent:
            self._parent._add_child(self)
    
    def _add_child(self, child_theme):        
        self._children[child_theme._match_class] = child_theme
        if self._parent:
            self._parent._add_child(child_theme)

    def _find_match_for(self, instance):
        for cls in self._children:
            if isinstance(instance, cls):
                return self._children[cls]._find_match_for(instance)        
        
        if isinstance(instance, self._match_class):
            return self
        elif self._parent:
            return self.parent._find_match_for(instance)
        else:
            return None

    def __setattr__(self, propname, value):
        if propname.startswith("_"):
            self.__dict__[propname] = value
        else:
            self.__dict__["__" + propname] = value
    
    def __getattr__(self, propname):        
        if propname.startswith("_"):
            return self.__dict__[propname]
        if ("__" + propname) in self.__dict__:
            return self.__dict__["__" + propname]
        elif self._parent:
            return getattr(self._parent, propname)
        else:
            return None


