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
Approach 1: 
```python
def SomethingThatCreateAFragmentOfAScene(showObject=Default):
    self = Sofa.Core.Node("A")
    self.addObject("MechanicalObject", name="state", showObject=objectObject)
    return self
```

Approach 2: 
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

Approach 3: 
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

