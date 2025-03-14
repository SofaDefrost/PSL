import unittest
from pslir import IRNode, PSLEntity, Prefab, Entry, Object
from pslbackend import serialize

import Sofa
import Sofa.Core
                 
def validate_and_print(fragment):
    print(fragment)
    exec(fragment)

class IRNodeTest(unittest.TestCase):
    def test_serialization_invalid_irnode_type(self):
        node1 = IRNode(name="node1", psl_instance=Entry(), type=Entry, creator=Sofa.Core.Node, children=[])     
        with self.assertRaises(Exception):
            serialize(node1)

    def test_serialization_valid_irnode_prefab(self):
        node1 = IRNode(name="node1", psl_instance=Prefab(), type=Prefab, creator=Sofa.Core.Node, children=[])     
        a = serialize(node1)
        
    def test_serialization_valid_irnode_object(self):
        node1 = IRNode(name="node1", psl_instance=Object("MechanicalObject"), type=Object, creator=Sofa.Core.Object, children=[])     
        a = serialize(node1)
        validate_and_print(a)
        
    def test_serialization_valid_irnode_prefab_in_prefab(self):
        node1 = IRNode(name="node1", psl_instance=Prefab(), type=Prefab, creator=Sofa.Core.Node, children=[]) 
        node2 = IRNode(name="node2", psl_instance=Prefab(), type=Prefab, creator=Sofa.Core.Node, children=[]) 
        node1.add_node(node2)
        a = serialize(node1)
        validate_and_print(a)
        
    def test_serialization_valid_irnode_object_in_prefab(self):
        node1 = IRNode(name="node1", psl_instance=Prefab(), type=Prefab, creator=Sofa.Core.Node, children=[]) 
        object1 = IRNode(name="object1", psl_instance=Object("MechanicalObject"), type=Object, creator=Sofa.Core.Object, children=[]) 
        node2 = IRNode(name="node2", psl_instance=Prefab(), type=Prefab, creator=Sofa.Core.Node, children=[]) 
        node1.add_node(object1)
        node1.add_node(node2)        
        a = serialize(node1)
        validate_and_print(a)

    def test_serialization_node(self):
        #node1 = IRNode(name="node1", psl_instance=Entry(), type=Entry, creator=Sofa.Core.Node, children=[]) 
        
        #print( serialize(node1) )
        pass

if __name__ == '__main__':
    unittest.main()
