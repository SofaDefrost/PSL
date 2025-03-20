import unittest
import pslir
from pslir import IRNode, PSLEntity, Prefab, Entry

import Sofa
import Sofa.Core

                
class IRNodeTest(unittest.TestCase):
    def test_constructor(self):
        node1 = IRNode(name="node1", psl_instance=Entry(), type=Entry, creator=Sofa.Core.Node, children=[]) 

    def test_children_add(self):
        node1 = IRNode(name="node1", psl_instance=Entry(), type=Entry, creator=Sofa.Core.Node, children=[]) 
        node2 = IRNode(name="node2", psl_instance=Entry(), type=Entry, creator=Sofa.Core.Node, children=[]) 

        node1.add_node(node2)

        self.assertEqual(len(node1.children), 1)

    def test_dump(self):
        node1 = IRNode(name="node1", psl_instance=Entry(), type=Entry, creator=Sofa.Core.Node, children=[]) 
        node2 = IRNode(name="node2", psl_instance=Entry(), type=Entry, creator=Sofa.Core.Node, children=[]) 
        node3 = IRNode(name="node3", psl_instance=Entry(), type=Entry, creator=Sofa.Core.Node, children=[]) 
        node4 = IRNode(name="node4", psl_instance=Entry(), type=Entry, creator=Sofa.Core.Node, children=[]) 
        node1.add_node(node2)
        node1.add_node(node3)
        node3.add_node(node4)
        
        print(str(node1))
        self.assertNotEqual( len(str(node1)), 0)

if __name__ == '__main__':
    unittest.main()
