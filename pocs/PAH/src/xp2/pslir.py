import dataclasses
try:
    from typing import Any, Self
except: 
    from typing_extensions import Self

class PSLEntity:
    pass 

class Prefab(PSLEntity):
    def __str__(self):
        raise Exception("Trying to generate a string for the base class")

class Object(PSLEntity):
    def __init__(self, name):
        self.name = name 

    def __str__(self):
        return self.name

class Entry(Prefab):
    def __str__(self):
        raise Exception("Trying to generate a string for the base class")

def prepend(prefix : str, content : str) -> str: 
    """Add the samre prefix to every line of content"""
    lines = content.splitlines()
    out = ""
    for line in lines:
        out += prefix+line+"\n"
    return out

@dataclasses.dataclass
class IRNode:
    """Stores the details of a level of the hierarchical representation"""

    name : str
    """Name of the entry in the sofa scene"""

    psl_instance : object
    """PSL instance for this entry"""

    type : type             # type: ignore  
    """Type of the entry, it must be PSL class"""

    creator : type          # type: ignore 
    """The function to create a new pslinstance"""

    children : list[Any]

    """List of the IRNode contained by this one"""
    def __post_init__(self):
        self.check_internal_type()

    def add_node(self, node : Self):
        self.children.append(node)

    def check_internal_type(self):
        """Insure that the given parameters fullfill the interface/type we expect"""
        assert( isinstance(self.name, str) )
        assert( isinstance(self.psl_instance, object) )
        assert( isinstance(self.type, type) )
        assert( isinstance(self.creator, object) )
        assert( isinstance(self.children, list) )

    def __repr__(self):
        cs = "" 
        for entry in self.children:
            cs += prepend("       ", str(entry))
        if len(self.children) == 0:
            cs = "       []"

        s = f"""{self.name}:
      type: {self.type}
   creator: {self.creator}
  instance: {self.psl_instance}
  children: 
{cs}"""
        return s
