import dataclasses
import inspect
import typing

def is_object_description(cls : type) -> bool:
    return issubclass(cls,SofaObject)

def is_node_description(cls : type) -> bool:
    return issubclass(cls,SofaNode)

@dataclasses.dataclass
class MemberInfo(object):
    name : str
    value : typing.Any
    type : type | None

    def __str__(self):
        return (str(self.name), str(self.value), str(type))


# Mock sofa classes . 
class SofaBase:
    name : str = "Unnamed"

    @classmethod
    def get_data_declared(cls) -> dict[str, MemberInfo]:        
        selected_members = {}
        for info in cls.get_members_declared().values():
            if info.type is not None:
                if info.type.is_data():
                    selected_members[info.name] = info
        return selected_members

    @classmethod
    def get_members_declared(cls) -> dict[str, MemberInfo]:
        attributes = {}
        for name, value in typing.get_type_hints(cls).items():  
            attributes[name] = MemberInfo(name, None, type=value)
           
        for name, value in inspect.getmembers(cls):  
            if not name.startswith('_'):
                if not inspect.ismethod(value) and not inspect.isfunction(value): 
                    if name in attributes:
                        attributes[name] = MemberInfo(name=name, value=value, type=None)
                    else:
                        attributes[name] = MemberInfo(name=name, value=value, type=attributes[name].type)
        return attributes

    @classmethod
    def clone(cls):
        """Deep clone of the cls, compare to simple duplication the initialized members are also copied"""
        attributes = {} 
        # Inspect static members 
        for i in inspect.getmembers_static(cls):  
            # to remove private and protected
            # functions
            if not i[0].startswith('_'):
                # Remove methods: 
                if not inspect.ismethod(i[1]): 
                    attributes[i[0]] = i[1]

        return type(cls.__name__+"Instance", (cls, ), attributes)

    @classmethod
    def is_data(cls): 
        return False

class LinkPath:
    pass 

class BaseData:
    @classmethod
    def is_data(cls):
        return True

# Here T is a generic type (if unused, just think of it as c++ template)
class DataValue[T](BaseData):
    value : T 
    linkpath : str
    
    def setParent(self): pass  

# Here T is a generic type (if unused, just think of it as c++ template)
class DataVector[T](BaseData):
    value : list[list[T]] 
    linkpath : str
    
    def setParent(self): pass  

class SofaNode(SofaBase):
    bbox : DataValue[float] 
    
    def addNode():
        return 

    def addObject():
        return 
            
class SofaObject(SofaBase):
    pass 

## Example of class declaration corresponding to MechanicalObject
@dataclasses.dataclass
class MechanicalObject(SofaObject):
    position : DataVector[float]
    rest_position : DataVector[float]

    showObject : DataValue[bool]

    def to_dict(self):
        return dataclasses.asdict(self)
