"""Describing SOFA components with type hints 
This pep is for describing Sofa components using the type hints and object declaration

This PEP use the eye-candy syntax for Generic type hints available since python 3.12 

The provided example is showing it without modification in SOFA. 

Several improvement are possible as demonstrated in the function "improvement_xxx"

Contributors: 
  - damien.marchal@univ.lille.fr   
"""
import Sofa.Core 
import dataclasses

class LinkPath:
    pass 

# Here T is a generic type (if unused, just think of it as c++ template)
class DataValue[T]:
    value : T 
    linkpath : str
    
    def setParent(self): pass  

# Here T is a generic type (if unused, just think of it as c++ template)
class DataVector[T]:
    value : list[list[T]] 
    linkpath : str
    
    def setParent(self): pass  

## Example of class declaration corresponding to MechanicalObject
class MechanicalObject(Sofa.Core.Object):
    name : str 
    "documentation here "

    position : DataVector[float]
    rest_position : DataVector[float]

    showObject : DataValue[bool]
    ... 

def createScene(root : Sofa.Core.Node):
    # The two following lines are monkey patching to demonstrate the API 
    def addObject[T](self, o : T, **kwargs ) -> T:
        return self.addObject(T.__class__.__name__, **kwargs)
    root.addObject = addObject

    ## Allow the addObject to be passed directly      
    q = addObject(root, MechanicalObject, name="object1")  
    q.position.value = [[2.0,3.0,4.0]]