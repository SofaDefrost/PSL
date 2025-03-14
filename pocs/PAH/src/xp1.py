import Sofa
import Sofa.Core
import pprint
import copy
from collections import OrderedDict
import typing


# Read this for better understanding.
# https://blog.ionelmc.ro/2015/02/09/understanding-python-metaclasses/
class A(type):
    def __setattr__(self, name, item):
        self.__annotations__[name] = item

    def __delitem__(self, item):
        del self.__annotations__[item]
        print("REMOVE item", item)

class PrefabParameters:
    def __init__(self):
        self.__dict__["parameters"] = {}

    def __setattr__(self, name, value):
        print("VALUE ", name, value)
        self.__dict__["parameters"][name] = value

    def __contains__(self, name):
        return name in self.__dict__["parameters"]

    def __getitem__(self, name):
        return self.__dict__["parameters"][name]
        
    def __getattr__(self, name):
        print("GET ", name)

        if name not in self.__dict__["parameters"]:
            print("CREATE ... ", name)
            self.__dict__["parameters"][name] = PrefabParameters()
        
        return self.__dict__["parameters"][name]
    
    def __str__(self):
        return str( self.__dict__["parameters"])

class Prefab(metaclass=A):
    __prefab_parameters__ : PrefabParameters
    type : Sofa.Core.Node

    def get_parameters(self):
        return self.__prefab_parameters__

    def connect(target):
        pass

    def __new__(cls, *args, **kwargs):
        o = object.__new__(cls) 
        p = PrefabParameters()
        o.__class__.connect(p)
        o.__prefab_parameters__ = p 
        return o 
    
    def __init__(self):
        print("INIT === >", self.__prefab_parameters__ )
        children={}
        objects={}
        data={}
        order=[]    

        attributes = get_class_attributes(self.__class__) 
        print("ANNOTATION", self.__annotations__)
        print("ATTRIBUTES ", attributes)

        for name, cls in self.__annotations__.items():
            if name != "type" and not name in attributes:
                print("CREATE SUB... ", name, cls.__name__)
                attributes[name] = cls()
                setattr(self, name, attributes[name])
            if name == "type":
                print("CREATE TYPE... ", name, cls.__name__)
                setattr(self,"type", cls)

        for cname, fragment in attributes.items():
            if cname == "type":
                continue
            if isinstance(fragment, Prefab): 
                children[cname] = fragment
                order.append(cname)
            elif isinstance(fragment, SofaObject):
                objects[cname] = fragment
                order.append(cname)
            else: 
                data[cname] = fragment
                order.append(cname)
    
        print("==========FOUND:")
        print("       children:"+str(children))
        print("         object:"+str(objects))
        print("           data:"+str(data))
        #       order)        


class SofaObject:
    __prefab_parameters__ : PrefabParameters

    def __new__(cls, *args, **kwargs):
        o = object.__new__(cls) 
        p = PrefabParameters()
        o.__class__.connect(p)
        o.__prefab_parameters__ = p 
        return o 
        
    def get_parameters(self):
        return self.__prefab_parameters__

    def connect(target):
        pass

class PointSet(SofaObject):
    type : Sofa.Core.Object = "PointSetTopologyContainer"
        
class TriangleSet(SofaObject):
    type : Sofa.Core.Object = "TriangleSetTopologyContainer"


class Mapping(SofaObject):
    @staticmethod
    def select_mapping(input, **kwargs):
        print("CREATING A MAPPING FROM INPUT ", input)
        return "RigidMapping"
    
    type : Sofa.Core.Object = select_mapping
    
class Renderer(SofaObject):
    type : Sofa.Core.Object = "OglModel"
    src : str 

class MechanicalObject(SofaObject):
    type : Sofa.Core.Object = "MechanicalObject"
    template : str = "Vec3"
    showObject : bool 

class Geometry(Prefab):
    type : Sofa.Core.Node 

    points : PointSet
    triangles : TriangleSet
    
class VisualModel(Prefab):
    type : Sofa.Core.Node

    geometry : Geometry 
    renderer : Renderer 
    mapping : Mapping

    template : str = "Rigid3"

def issub(a, ttype):
    if not hasattr(a, "__annotations__"):
        return False
    t = a.__annotations__["type"]
    if t == ttype:
        return True
    return False    

def iskindof(a, ttype):
    if not hasattr(a, "__annotations__"):
        return False
    t = a.__annotations__["type"]
    if t == ttype:
        return True
    return False    

def get_class_attributes(cls):
    ca = {}

    print("GET CLASS ATTRIBUTES.... ", cls)
    for attribute in cls.__dict__.keys():
        if attribute[:2] != '__':
            value = getattr(cls, attribute)
            if not callable(value):
                ca[attribute] = value
    return ca
        
def instantiateObject(cls, node, name,space=""):
    # Get the annotation... 
    #fragments = fragment.__annotations__
    print(space+"Instantiation of new object", name, cls, node)
    space+="  "
    if cls.__class__ == type:
        attributes = get_class_attributes(cls) 
    else:
        attributes = get_class_attributes(cls.__class__) 
        
    print(space+"attributes", attributes)
    creator = attributes["type"]
    print(space+"creator", creator)
    #fragment, fragment.__annotations__, attributes)

    children={}
    objects={}
    data={}
    order=[]    
    for cname, fragment in attributes.items():
        if cname == "type":
            continue
        if isinstance(fragment, SofaPrefab): 
            children[cname] = fragment
            order.append(cname)
        elif isinstance(fragment, SofaObject):
            objects[cname] = fragment
            order.append(cname)
        else: 
            data[cname] = fragment
            order.append(cname)
    
    print(space+"    FOUND, ", children, objects, data, order)        

    node.addObject(creator, name=name, **data)

def instantiate(pslinstance : object, parent, name=None, space=""):
    #print(psl.__annotations__)

    psl = pslinstance.__class__

    # Compute the name from the class name 
    if name == None:
        name = psl.__name__

    print(space+"NODE: ", name)
    space+="   "
    # Get the annotation... 
    fragments = psl.__annotations__
    creator = fragments["type"]
    
    children = {}
    objects = {}
    data = {}
    order = []

    for cname, fragment in fragments.items():
        if cname == "type":
            continue
        if issub(fragment, Sofa.Core.Node): 
            children[cname] = fragment
            order.append(cname)
        elif iskindof(fragment, Sofa.Core.Object):
            objects[cname] = fragment
            order.append(cname)
        else: 
            data[cname] = fragment
            order.append(cname)

    # Override the class with an instance
    for cname, value in psl.__dict__.items():
        #print(space+"SEARCHING ", cname, value)
        if cname in children:
            print(space+"    PATCHING ", cname)
            children[cname] = value 
        if cname in objects:
            print(space+"    PATCHING ", cname)
            objects[cname] = value            
        

    if creator == Sofa.Core.Node: 
        print(space+"Create node ", name)
        print(space+"  with context ", children, objects, data, order)        
        self = parent.addChild( creator(name) )

        #for pchild in order:
        #    if pchild in objects:
        
        for name in order:
            print(space+"  PROCESSING ", name, objects, children)
            if name in objects:
                print(space+"LOOK IN CLASS ", objects[name] )
                
                #if isinstance(getattr(name), class):
                instantiateObject(objects[name], node=self, name=name,space=space+"    ")

            if name in children:
                print(space+"CREATE SUB NODE WITH NAME ", name, children[name])
                if not hasattr(pslinstance, name) or not isinstance(getattr(pslinstance, name), object):
                    xx = children[name]()
                    print(space+"NON INITIALIZED OBJECT. LET'S CREATE AN EMPTY ONE ", xx )
                    setattr(pslinstance, name, children[name]())
                instantiate(getattr(pslinstance, name), parent=self, name=name, space=space+"    ")

        #for pchild in order:
        #    if pchild in children:
        #        instantiate(children[pchild], parent=self)

def get_details(attributes):
    children={}
    objects={}
    data={}
    order=[]    
    for cname, value in attributes.items():
        if cname == "type":
            continue
        if isinstance(value, Prefab): 
            children[cname] = value
            order.append(cname)
        elif isinstance(value, SofaObject):
            objects[cname] = value
            order.append(cname)
        else: 
            data[cname] = value
            order.append(cname)
    return {"children" : children, "objects": objects, "data":data, "order":order }

def to_ir(pslcls : Prefab, parent, name=None, params=PrefabParameters()) -> dict:
    print("======================================== TO IR ===========================")
    attributes = get_class_attributes(pslcls) 
    details = get_details(attributes)
    print("  CREATE TYPE: ", pslcls.type)
    print("  ATTRIBUTES... ", attributes)
    print("  DETAILS... ", details)
    print("  PREFAB PARAMS... ", pslcls.get_parameters())
    
    if name is None:
        name = pslcls.__class__.__name__
    
    entry = OrderedDict()
    entry["self"] = pslcls
    entry["creator"] = pslcls.type
    entry["type"] = pslcls.__class__
    entry["children"] = OrderedDict()
    entry["data"] = {"name": name} 

    for name in details["order"]:
        if name in details["objects"]:
            v = details["objects"][name]    # We have here the object poited. 
            print("    Processing OBJECT "+str(name), v, get_class_attributes(v))
            lparam = {}
            
            if name in params:
                print("YO GET PARAMS FOR ", name, params[name])
                lparam = params[name] 
            entry["children"][v] = to_ir(v, parent, name, params=lparam)

        elif name in details["children"]:
            v = details["children"][name]    # We have here the object poited. 
            print("    Processing CHILDREN "+str(name), v)
            entry["children"][name] = to_ir(v, parent, name)
    
    entry["params"] = params
    entry["data"]  |= details["data"]

    return entry

def instantiate(pslir, parent):
    # Let's build the kwargs of the object  
    print("======================================== TO SOFA ===========================")
    print(pslir)
    print("=========================== ")
    kwargs = {}
    for k,v in pslir["data"].items():
        kwargs[k] = v
    
    if isinstance(pslir["params"], PrefabParameters):
        for k,v in pslir["params"].__dict__["parameters"].items():
            kwargs[k] = v
    else:
        for k,v in pslir["params"].items():
            kwargs[k] = v
            
    print("KWARGS: ", pslir["self"], kwargs)

    if isinstance(pslir["self"], Prefab):
        sofanode = parent.addChild(kwargs["name"])
        for child, value in pslir["children"].items():
            instantiate(value, sofanode)
    else:
        creator = pslir["creator"]
        if callable(creator):
            creator = creator(parent, **kwargs) 
        parent.addObject(creator, **kwargs)


def dump_ir(ir):
    pprint.pprint(ir)

def createScene(root):

    class Tripod(Prefab): 
        type : Sofa.Core.Node
        state : MechanicalObject = MechanicalObject()
        visual : VisualModel = VisualModel()

    #desc = Tripod()
    #desc.state.template = "Rigid3"

    #M = typing.TypeVar('M')
    #class YOLO(Prefab, typing.Generic[M]):
    #    mapping : M 

    class Data(object):
        pass

    class Test(Prefab):
        type : Sofa.Core.Node
        
        #### This is an object
        state : MechanicalObject

        #### This is a child
        visual : VisualModel # = {"template" : "@state.template"} # type: ignore
        
        angle : float

        def connect(self):
            self.state.template = "Rigid3"
            self.state.showObject = True
            
            self.visual.renderer.src = "@visual.geometry.triangles"

    class Modelling(Prefab):
        type : Sofa.Core.Node 
        test1 : Test 
        test2 : Test

        link : str = "@toto"

 

    #modelling = Modelling()
    #modelling.test1.state.template = "Rigid3"
    #modelling.test2.state.template = "Rigid3"

    #ir = to_ir(modelling, root) 
    #instantiate(ir, root) 

    # A new prefab generated from the Modelling template
    #Modelling2 = copy.copy(Modelling)
    # del Modelling2["test2"]    
    # Modelling2.test3 = Test
    
    pls = Modelling()
    ir = to_ir(pls, root, params=pls.get_parameters()) 
    dump_ir(ir)
    instantiate(ir, root) 

