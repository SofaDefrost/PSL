Python Annotation Hacking
=========================

In several PEP and discussion it was envisioned that the python syntax with type annotation would 
serve as a sofa scene description langage. So here is the corresponding POC. 

This POC is related with:
- PEP #12 
- ... 

We would like to see if we can implement most of the PEP > 12 features on top of a syntaxe like the following 

```python
class VisualModel(Sofa.Core.Prefab):
    state : MechanicalObject 
    
    enable : Data[bool]
    """bla bla""" 
```

