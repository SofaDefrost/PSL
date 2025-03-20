Using Python Dictionnary as Scene Langage
=========================================

If we describes scene/prefab as python dictionnary, is there any interest to a scene loader to process them.

```python
def load(scene, root):
    for k,v in scene.items():
        if k == "Node":
            c=root.addChild()
            load(c, ... )
        else:
            root.addObject(k, **v)
    return ..

def createScene(root):
    scene = {
        "Node" : 
            "MechanicalObject" : 
                { "name" : "toto" }
   }

   load(scene, root)
```

   