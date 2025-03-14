# This PEP only works after python3.12 because it use the new generic type variable syntax
# Backward compatibility can be implemented but it results in a more invasive syntax
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


# Use with SofaPython3 API v24.12  
m = root.addObject(MechanicalObject, name="object1")  # type: MechanicalObject
    
# The two following lines are monkey patching to demonstrate how the SofaPython API     
# should be changed to allow more clean syntax 
def addObject[T](self, o : T, **kwargs ) -> T:
    return self.addObject(T.__class__.__name__, **kwargs)
root.addObject = addObject

## Allow the addObject to be passed directly      
q = root.addObject(MechanicalObject)  
q.position.value = [[2.0,3.0,4.0]]

