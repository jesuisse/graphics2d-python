import unittest
import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from graphics2d.themes import *

class A():
    pass

class B():
    pass

class C(A):
    pass

class D(C):
    pass

class TestThemes(unittest.TestCase):

   
    def test_find_theme_match(self):
        # Create a base theme
        x = Theme(match_class = A)
        # add y (class B default theme) to the base theme
        y = Theme(match_class = B, parent=x)
        # add z (class C default theme) to the base theme
        z = Theme(match_class = C, parent=x)
        
        a = A()
        b = B()
        c = C()
        d = D()
        
        # now have these instances find the theme that
        # applies to them
        
        # the best match for the base class is it's default theme x
        self.assertEqual(x._find_match_for(a), x)
        
        # the best match for b is it's default theme y
        self.assertEqual(x._find_match_for(b), y)
        
        # the best match for c is it's default theme z
        self.assertEqual(x._find_match_for(c), z)
        
        # the best match for d is z (its parent class default theme)
        self.assertEqual(x._find_match_for(d), z)

    def test_set_prop(self):
        x = Theme(match_class = A)
        z = Theme(match_class = C, parent=x)
        x.font = "Font"
        z.fontsize = 24
        self.assertEqual(x.font, "Font")
        self.assertEqual(z.fontsize, 24)

    def test_get_own_prop(self):
        x = Theme(match_class = A)
        x.font = "Font"        
        self.assertEqual(x.font, "Font")

    def test_get_parent_prop(self):
        x = Theme(match_class = A)
        z = Theme(match_class = C, parent=x)
        x.font = "Font"    
        self.assertEqual(z.font, "Font")

    def test_get_overriden_prop(self):
        x = Theme(match_class = A)
        z = Theme(match_class = C, parent=x)
        x.font = "Font"        
        z.font = "Another Font"
        self.assertEqual(z.font, "Another Font")

    def test_get_nonexistent_prop(self):
        x = Theme(match_class = A)
        z = Theme(match_class = C, parent=x)
        x.font = "Font"        
        z.font = "Another Font"
        self.assertEqual(z.fontsize, None)

    def test_get_overriden_prop_in_base(self):
        x = Theme(match_class = A)
        z = Theme(match_class = C, parent=x)    
        z.font = "Another Font"
        self.assertEqual(x.font, None)

    def test_full_demo_lookup(self):
        # We create a base theme and a default theme for class C
        x = Theme(match_class = A)
        z = Theme(match_class = C, parent=x)
        # the base theme has a font property defined.
        x.font = "Font"
        # d is an instance of a class which derives from C
        d = D()
        # theme will find the default theme z for class C
        theme = x._find_match_for(d)
        self.assertEqual(theme, z)
        # and this will use the parent theme x's value for the font 
        self.assertEqual(theme.font, "Font")
        

if __name__ == '__main__':
    unittest.main()