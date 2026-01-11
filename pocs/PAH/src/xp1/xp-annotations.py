import typing

class Prefab(object):
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        
        if not hasattr(cls, "__orig_bases__"):
                cls.templates = {}
                return 
        

        args = typing.get_args(cls.__orig_bases__[1])
        print("= ==== > ", cls, typing.get_type_hints(cls))

        print(" ----------->", typing.get_type_hints(cls))
        cls.args = typing.get_type_hints(cls)
        cls.templates = None

    def get_templates(self):
        values = []
        if not hasattr(self, "__orig_class__"):
            if not hasattr(self, "__orig_bases__"):
                return 
            values += [ variabletype for variabletype in typing.get_args(self.__orig_bases__[-1]) ]
        
        if hasattr(self, "__orig_class__"):
            values += typing.get_args(self.__orig_class__)

        names = self.__class__.args
        print("VALUES.... ", names, values )
        if self.__class__.templates is None:
            self.__class__.templates = {}
            for name, variable in names.items():
                value = variable
                self.__class__.templates[name] = (value.__default__, type(value))
        return self.templates
        

X = typing.TypeVar("X", default=int)
B = typing.TypeVar("B", default=float)

class AClass(Prefab, typing.Generic[X,B]):
    i : X
    b : B
    pass

class Rigid3:
    pass
class Vec3: 
    pass 

Template = typing.TypeVar("Template", default=Rigid3)
Template2 = typing.TypeVar("Template2", default=Vec3)

class MechanicalObject(Prefab, typing.Generic[Template, Template2]):
    template : Template
    template2 : Template2
    
    positions : list[int] 

BClass = AClass[MechanicalObject[Rigid3, Vec3], int]

print(type( AClass ))

print(dir( BClass ))
print(dir(type( BClass )))

print(AClass.__annotations__)

b = BClass()
print("get_origin(BClass)", typing.get_origin(BClass))
print("get_args(BClass)", typing.get_args(BClass))

print("get_origin(self.)", typing.get_origin(b))
print("get_args(self)", typing.get_args(b))

print("get_origin(self.__class__)", typing.get_origin(b.__class__))
print("get_args(self.__class__)", typing.get_args(b.__class__))

print("b ", b)
print("b type", type(b))
print("b ", type(b.__class__))

print(b.__annotations__) 
print("getTemplate", MechanicalObject().get_templates())
