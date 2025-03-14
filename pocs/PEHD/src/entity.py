from typing import Callable, Optional, overload

import Sofa
import Sofa.Core
import dataclasses

DEFAULT_VALUE = object()

def NONE(*args, **kwargs):
    pass

def to_dict(o):
    if isinstance(o, dict):
        return o
    if hasattr(o, "to_dict"):
        return o.to_dict()
    return {}

@dataclasses.dataclass
class PrefabParameters(object): 
    name : str = "Prefab"
    kwargs : dict = dataclasses.field(default_factory=dict)

    def __getattr__(self, name: str) :
        if name == "__getstate__":
            getattr(PrefabParameters, "__getstate__")
        if name == "__setstate__":
            getattr(PrefabParameters, "__setstate__")

        try: 
            a =  self.__getattribute__(name)
        except Exception as e: 
            return NONE
        return a

    def to_dict(self):
        t =  dataclasses.asdict(self)
        del t["kwargs"]
        return t | self.kwargs


class SofaPrefab(Sofa.Core.Node):
    name : str
    parameters : PrefabParameters

    def __init__(self, 
                 parent : Sofa.Core.Node = None, 
                 parameters : PrefabParameters = PrefabParameters()):
        
        # BUG: The API in sofa does not allow to pass kwargs in node constructor. Report a bug in sofapython 
        Sofa.Core.Node.__init__(self, name=parameters.name)

        self.initialize(parent, parameters)
        self.instantiate()
        self.check_prefab_contract()

    def initialize(self, parent, parameters):
        if parent != None:
            parent.addChild(self)
        self.parameters = parameters

        self.do_initialize(parent, parameters)

    def instantiate(self):
        self.do_instantiate(self.parameters)

    def check_prefab_contract(self):
        """This function validates all the structural condition the object must match"""

        import inspect
        mro = inspect.getmro(type(self))
        for cls in mro:
            if issubclass(cls, Sofa.Core.Prefab):
                print("DO LYSKOV CHECKING AT LEVEL ", cls)
                cls.do_check_prefab_contract(self)

    def do_initialize(self, parent, parameters):
        pass 

    def do_instantiate(self, parameters):
        pass 

    def do_check_prefab_contract(self):
        assert( hasattr(self, "name") ) 
        assert( hasattr(self, "parameters") ) 

# MONKEY PATCH: remove 
Sofa.Core.Prefab = SofaPrefab 


def addGeometry(geometry, parameters):
    print("DUMP " , to_dict(parameters))
    geometry.addObject("PointSetTopologyContainer", **to_dict(parameters.points))
    geometry.addObject("TriangleSetTopologyContainer", **to_dict(parameters.triangles))

@dataclasses.dataclass
class GeometryParameters(PrefabParameters):
    name : str = "geometry"
    addGeometry : Callable = addGeometry

    points : PrefabParameters = PrefabParameters(name="points")
    triangles : PrefabParameters = PrefabParameters(name="triangles")

class Geometry(Sofa.Core.Prefab):
    def __init__(self, parent : Sofa.Core.Node = None, parameters : GeometryParameters = GeometryParameters()):
        Sofa.Core.Prefab.__init__(self, parent = parent, parameters=parameters)

    def do_instantiate(self):
        self.parameters.addGeometry(self, self.parameters) 

@dataclasses.dataclass
class GeometryFromFileParameters(GeometryParameters):
    filename : str = "mesh/sphere_01.obj"

class GeometryFromFile(Geometry):
    loader : Sofa.Core.Object 

    def __init__(self, parent=None, parameters : GeometryFromFileParameters = GeometryFromFileParameters(), filename = None):
        if filename != None:
            parameters.filename = filename
        Geometry.__init__(self, parent=parent, parameters=parameters)
    
    def do_instantiate(self, parameters : GeometryFromFileParameters):
        self.addGeometryFromFile(parameters=parameters)

    def do_check_prefab_contract(self):
        """ This is a geometry... with filename """
        print("TO DO: Check contract")

    def addGeometryFromFile(self, parameters : GeometryFromFileParameters):
        print("PARAMETERS ", to_dict(parameters))
        self.addObject("MeshOBJLoader", name=parameters.name, filename=parameters.filename)
        addGeometry(self, parameters=parameters)

@dataclasses.dataclass
class VisualModelParameters(PrefabParameters):
    name : str = "VisualModel"

    template : Optional[str] = None #"Rigid3"

    renderer : dict = dataclasses.field(default_factory=dict)
    mapping : dict = dataclasses.field(default_factory=dict)

    geometry : GeometryParameters = GeometryParameters()

class VisualModel(Sofa.Core.Prefab):
    geometry : Sofa.Core.Object
    renderer : Sofa.Core.Object
    mapping : Sofa.Core.Object
        
    def __init__(self, parent : Sofa.Core.Node = None, 
                       parameters : VisualModelParameters = VisualModelParameters()):
        Sofa.Core.Prefab.__init__(self, parent=parent, parameters=parameters)
        
    def do_initialize(self, parent, parameters):
        template = "Rigid3"
        if parameters.template is None:
            if parent != None:
                template = parent.state.getTemplateName()        
        else:
            template = parameters.template                
        self.template = template

    def do_instantiate(self, parameters): 
        print("INSTANTIATE ", to_dict(parameters))       
        self.addGeometry(parameters=parameters.geometry)
        self.addRenderer(**to_dict(parameters.renderer) | {"src" : "@geometry"} )
        self.addMapping(**to_dict(parameters.mapping) )

    def do_check_prefab_contract(self):
        """This function validates all the structural condition the object must match"""
    
        assert hasattr(self, "geometry" ), "There must be a geometry"
        assert hasattr(self, "renderer" ), "There must be a renderer"
        assert hasattr(self, "mapping" ), "There must be a mapping"

    def addGeometry(self, parameters : GeometryParameters):
        print("ADD .. ", to_dict(parameters), " to " , str(type(self)))
        parameters.addGeometry(self, parameters)

    def addRenderer(self, **kwargs):
        self.addObject("OglModel", name="renderer", **kwargs)

    def addMapping(self, **kwargs):
        name = "RigidMapping"
        if self.template == "Vec3d":
            name = "IdentityMapping"
        self.addObject(name, name="mapping", **kwargs)
        
class CollisionModel(Sofa.Core.BasePrefab):
    def __init__(self, params, **kwargs):
        Sofa.Core.Node.__init__(self, **kwargs)

    class Parameters(object):
        enabled : bool = False 

@dataclasses.dataclass
class SimulationParameters(PrefabParameters):
    name : str = "Simulation"
    iterations : Optional[int] = None 
    template: Optional[str] = None 
    solver : dict = dataclasses.field(default_factory=dict)
    integration : dict = dataclasses.field(default_factory=dict)

    def to_dict(self):
        return self.asdict() 

class Simulation(Sofa.Core.Node):
    solver : Sofa.Core.Object 
    integration : Sofa.Core.Object
    iterations : int

    def __init__(self, parent : Sofa.Core.Node = None, parameters : SimulationParameters = SimulationParameters()):
        Sofa.Core.Node.__init__(self, name=parameters.name)
        
        if parent is not None:
            parent.addChild(self)
    
        if parameters.iterations != NONE and "iterations" in parameters.solver:
            raise Exception("Cannot set direct attribute and internal hack... ")

        self.addObject("EulerImplicitSolver", name = "integration", **to_dict(parameters.integration))
        self.addObject("CGLinearSolver", name = "solver", iterations=parameters.iterations, **to_dict(parameters.solver))


@dataclasses.dataclass
class MechanicalParameters(PrefabParameters): 
    name : str = "state"
    position : list[list[float]]  = dataclasses.field(default_factory=list)
    template : str = "Vec3"

@dataclasses.dataclass
class EntityParameters(PrefabParameters): 
        name : str = "Entity"

        addSimulation : Callable = Simulation
        addCollisionModel : Callable = CollisionModel
        addVisualModel : Callable = VisualModel 

        #constitutive_law : 
         # : Callable = addBidule
        #setBoundaryCondition #: Callable = addBidule
        
        mechanical : MechanicalParameters = MechanicalParameters() 
        collision : CollisionModel.Parameters = CollisionModel.Parameters()
        visual : VisualModelParameters = VisualModelParameters()
        simulation : SimulationParameters = SimulationParameters()
        
class Entity(Sofa.Core.Node): 
    # A simulated object
    simulation : Simulation
    visual : VisualModel
    collision : CollisionModel
    
    parameters : EntityParameters

    def __init__(self, parent=None, parameters=EntityParameters(), **kwargs):
        Sofa.Core.Node.__init__(self, name=parameters.name)        

        if parent is not None: 
            parent.addChild(self)
        
        self.parameters = parameters

        if len(parameters.mechanical.position) == 0:
            if parameters.mechanical.template == "Vec3":
                parameters.mechanical.position = [[0,0,0]]
            else:
                parameters.mechanical.position = [[0,0,0, 0,0,0,1]]

        self.addMechanicalModel(**to_dict(parameters.mechanical))
        self.addSimulation(parameters=parameters.simulation)
        self.addVisualModel(parameters=parameters.visual)
        self.addCollisionModel()

    def addMechanicalModel(self, **kwargs): 
        self.addObject("MechanicalObject", **kwargs)

    def addSimulation(self, **kwargs): 
        self.parameters.addSimulation(self, **kwargs)

    def addVisualModel(self, **kwargs):
        self.parameters.addVisualModel(self, **kwargs)

    def addCollisionModel(self):
        pass 

class Rigid(Entity):
    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)    


class Deformable(Entity):
    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)    

@dataclasses.dataclass
class DeformableEntityParameters(EntityParameters):     
    addConstitutiveLaw : Callable = lambda x: x

    mass : Optional[float] = None    

    def to_dict(self):
        return dataclasses.asdict(self)



