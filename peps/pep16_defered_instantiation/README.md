Late Instanciation
==================

A lot of problem in python scene design come from the fact that the python API is an immediate mode 
in which Sofa objects are created on the fly. The consequence is that the scene must but "valid" at 
any time. This a strong consequences on how sofa component are implemented (mostly in term of robustness regarding the init/reinit/late init and data changes). 

In this PEP we are considering to have a deffered mode in which the actual creation of Sofa object is 
post-pone.  This PEP is build on top of having a scene description (as is the PEP)

```python 

def instanciate(scene, root):
    json_scene_loader( to_json(scene), root )

def createScene(root : Sofa.Core.Node)   
   import Sofa.Defered.Core

   s = Sofa.Defered.Core("root")
   n = s.addNode("child")
   n.addObject("MechanicalObject") 
   ... 

   instanciate(s, root)    
```