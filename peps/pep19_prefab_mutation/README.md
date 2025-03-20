Prefab Extension by Mutation
============================

Could it be possible, and if possible, is there any interest in extending a prefab through mutation instead of in-heritance

```python
   
class MyPrefab(Sofa.Core.Node):
       state : MechanicalObject
       loader : BaseLoader

       addCollision : Callable = lambda x: return "CollisionModel"
       addLoader : Callable = lambda x: return "Loader"
       
       addMechanicalForceField : Callable = lambda x: return "HexahedronForceField" 
       """ XXXX """

       addCollisionModel : 

def createScene(root):    
    
    # A change on the class is for all use of the class
    MyPrefab.addMechanicalForceField = lambda x : return "TetrahedronForceField

    # To make the change for only one case one must create a subtype 
    # Manually 
    MyCustomPrefab = MyPrefab.mutate()
    MyCustomPrefab.addMechanicalForceField = lambda x : return "TetrahedronForceField

    # Or by in-heritance 
    class MyCustomPrefab2(MyPrefab):
        addMechanicalForceField = lambda x : return "TetrahedronForceField" 

    root.add(MyPrefab)           # each of these will use 
    root.add(MyPrefab)
    root.add(MyCustomPrefab1)
    root.add(MyCustomPrefab2)
```

Comment: 
- if mutation and in-heritance are functionnaly equivalent, is there good practices to promote (like small changes => mutation, big change => in-heritance) 
- could we add structural constraints on the addXXX function to make clear what they are allowed to do. 