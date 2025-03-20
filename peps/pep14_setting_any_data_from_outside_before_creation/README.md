Setting Any Data from Outside Before the Creation
=================================================

It is straighforward to set data from the outside, after the object creation, as in the two examples
```python
def SomethingThatCreateAFragmentOfAScene(parent):
    self = parent.addChild("A")
    self.addObject("MechanicalObject", name="state")
    return self

def createScene(root):
  obj = SomethingThatCreateAFragmentOfAScene(root)
  obj.showObject = True
  obj.set(showObject=True, showScale=True)
```

```python
def SomethingThatCreateAFragmentOfAScene(mstate : MechanicalState):
    self = Sofa.Core.Node("A")
    self.addObject("MechanicalObject", name="state")
    return self

def createScene(root):
  obj = SomethingThatCreateAFragmentOfAScene()
  obj.showObject = True
  root.addChild( obj )
```
But these approach have drawback because several sofa component cannot updates their internal state/behavior once inited first.

The other approach is to set the parameters before the creation. 
Approach 1: passing changes as explicit prefab parameters
```python
def SomethingThatCreateAFragmentOfAScene(showObject=Default):
    self = Sofa.Core.Node("A")
    self.addObject("MechanicalObject", name="state", showObject=objectObject)
    return self
```

Approach 2: passing changes to component as a dictionary and prefab parameters with explicit arguments
```python
def SomethingThatCreateAFragmentOfAScene(filename : "sphere.obj", **kwargs): 
    self = Sofa.Core.Node("A")
    if filename.endswith("obj")
      self.addObject("MeshObjLoader", name="loader", filename=filename, **kwargs["loader"])
    else:
      self.addObject("MeshVtkLoader", name="loader", filename=filename, **kwargs["loader"])

    self.addObject("MechanicalObject", name="state", **kwargs["state"])
    return self

def createScene(root):
    a = SomethingThatCreateAFragmentOfAScene(filename="cube.vtk", {"state" : "showObject" = True})
    root.addChild(  )
```

Approach 3: passing both prefab argument and component's one with a dictionary 
```python
def SomethingThatCreateAFragmentOfAScene(parameters={}): 
    self = Sofa.Core.Node("A")
    if parameters["loader"]["filename"]:
      self.addObject("MeshObjLoader", name="loader", filename=filename, **kwargs["loader"])
    else:
      self.addObject("MeshVtkLoader", name="loader", filename=filename, **kwargs["loader"])

    self.addObject("MechanicalObject", name="state", **kwargs["state"])
    return self

def createScene(root):
    a = SomethingThatCreateAFragmentOfAScene({ "loader" : { "filename" : "sphere.obj" }, 
                                               "state" : {"showObject" = True} })
    root.addChild( a )
```

Approach 4: structuring the possible prefab parameters and internal prefab structure using classes and typehint.
            with extra arguments as dictionnary  
```python
class BaseLoaderParameters(Parameters):
  filename : str
  extras : {} 
  ...  

class MechanicalObjectParameters(Parameters):
  filename : str
  extras : {} 
  ...  

class MyPrefabParameters(Parameters):
  youngModulus : float
  poissonRatio : float 
  loader : BaseLoader  
  state : MechanicalObject
  mechanicallaw : TetrahedronFemForceField
  ...

class MyPrefab(Sofa.Node.Core):
  loader : BaseLoader  
  state : MechanicalObject
  mechanicallaw : TetrahedronFemForceField
  
  def __init__(self, p : MyPrefabParameters):
    self = Sofa.Core.Node("A")
    
    if p.loader.filename:
      self.addObject("MeshObjLoader", name="loader", p.loader)
    else:
      self.addObject("MeshVtkLoader", name="loader", p.loader)

    self.addObject("MechanicalObject", name="state", p.state)
    
def createScene(root):
    m = MyPrefabParameters({"loader.filename" : "cube.obj" })
    m.loader.filename = "cube.obj"
    m.state.showObject = True
    root.addChild( MyPrefab(m) )

    a = root.add( MyPrefab, m )
```