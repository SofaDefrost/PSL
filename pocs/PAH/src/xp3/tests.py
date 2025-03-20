import types
import unittest
from lib import *
import inspect 

class MainTests(unittest.TestCase):
    def test_class_attribute(self):
        """Initialization of attribute
        
           In case of in-heritance, the static class base attribute is only used when the child class
           is created. 
        """
        s = SofaObject
        SofaObject.name = "Unnamed" 
        self.assertEqual(s.name, "Unnamed")
        self.assertEqual(SofaBase.name, "Unnamed")

        SofaBase.name = "Named"
        self.assertEqual(SofaBase.name, "Named")
        self.assertEqual(SofaObject.name, "Unnamed")  
        
    def test_class_default_attribute(self):
        """Simple initialization of attribute"""
        SofaBase.name = "Named"
        s = SofaObject
        SofaObject.name = "Unnamed" 
        self.assertEqual(s.name, "Unnamed")
        self.assertEqual(SofaBase.name, "Named")

    def test_class_and_instance_change(self):
        """Change the value of an attribute of the instance"""
        # Set the SOfaObject name 
        SofaObject.name = "default"

        class AComponent(SofaObject):
            pass 
        s = AComponent() 

        self.assertEqual(SofaObject.name, "default")     # Access the class attributes... 
        self.assertEqual(s.name, "default")              # Access the class attributes...  (fallbacks)

        s.name = "instance"   # Change the instance content 
        self.assertEqual(s.name, "instance")             # A new instance attribute is added    
        self.assertEqual(SofaObject.name, "default")     # Access the class attributes... 

    def test_clone(self):
        """Clone is supposed to create a duplicated class out of the current one
           This is quite challenging because as python is copying something this include the 
           presence of attributes as well as there absence... in case of the absence of a class 
           attribute this fallback to the the parent one through getattribute
        """
        SofaObject.name = "default"
        class AComponent(SofaObject):
            enable : bool 

        class CComponent(SofaObject):
            name = "override"
            enable : bool 

        BComponent = AComponent.clone()                   # When cloning ... cut connexion with existing attrib's name 

        self.assertEqual(SofaObject.name, "default")      # EXPECTED
        self.assertEqual(AComponent.name, "default")      # EXPECTED 
        self.assertEqual(BComponent.name, "default")      # EXPECTED
        self.assertEqual(CComponent.name, "override")     # EXPECTED

        SofaObject.name = "basename"
        self.assertEqual(SofaObject.name, "basename")     # EXPECTED 
        self.assertEqual(AComponent.name, "basename")     # EXPECTED
        self.assertEqual(BComponent.name, "default")      # EXPECTED
        self.assertEqual(CComponent.name, "override")     # EXPECTED

        AComponent.name = "childname"                     # Create a new "name" attribute in class AComponent 
        self.assertEqual(SofaObject.name, "basename")     # EXPECTED 
        self.assertEqual(AComponent.name, "childname")    # EXPECTED 
        self.assertEqual(BComponent.name, "default")      # EXPECTED: still the same value when the copy was done. 
        self.assertEqual(CComponent.name, "override")     # EXPECTED 

        BComponent.name = "lastname"                      # Create a new "name" attribute in class BComponent 
        self.assertEqual(SofaObject.name, "basename")     # EXPECTED
        self.assertEqual(AComponent.name, "childname")    # EXPECTED   
        self.assertEqual(BComponent.name, "lastname")     # EXPECTED 
        self.assertEqual(CComponent.name, "override")     # EXPECTED 
        
    def test_is_object_predicate(self):
        class AComponent(SofaObject):
            enable : bool 
        self.assertTrue( is_object_description(SofaObject) ) 

        DComponent = AComponent.clone()
        self.assertTrue( is_object_description(SofaObject) ) 

        class CComponent(SofaNode):
            enable : bool 
        self.assertFalse( is_object_description(CComponent) )   

        DComponent = CComponent.clone()
        self.assertFalse( is_object_description(CComponent) )  

    def test_is_node_predicate(self):
        class AComponent(SofaObject):
            enable : bool 
        self.assertFalse( is_node_description(AComponent) ) 

        DComponent = AComponent.clone()
        self.assertFalse( is_node_description(DComponent) ) 

        class CComponent(SofaNode):
            enable : bool 
        self.assertTrue( is_node_description(CComponent) )  

        DComponent = CComponent.clone()
        self.assertTrue( is_node_description(DComponent) ) 
    
    def test_base_get_members_declared(self):
        class OglModel(SofaObject):
            datatype : str = "Vec3"

        class VisualModel(SofaNode):
            datatype : str = "Rigid3"
            renderer : OglModel 

        self.assertEqual( set(VisualModel.get_members_declared().keys()), set(["renderer", "datatype", "name", "bbox"]) ) 

    def test_base_get_data(self):
        class OglModel(SofaObject):
            datatype : str = "Vec3"

        class VisualModel(SofaNode):
            datatype : str = "Rigid3"
            renderer : OglModel 

        self.assertEqual( set(VisualModel.get_data_declared().keys()), set(["bbox"]) ) 


if __name__ == '__main__':
    unittest.main()
