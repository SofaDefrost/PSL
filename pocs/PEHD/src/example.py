import Sofa.Core
import copy
import entity
from entity import PrefabParameters, EntityParameters, Entity, Simulation, GeometryFromFileParameters


oldAdd=Sofa.Core.Node.addObject
def myAddObject(self : Sofa.Core.Node, tname, **kwargs):
    kwargs = copy.copy(kwargs)
    previouslen = len(self.objects) 
    try:
        oldAdd(self, tname, **kwargs)
    except Exception as e:
        target = self
        if len(self.objects) != previouslen:
            target = list(self.objects)[-1]
        Sofa.msg_error(target, str(e))
        
Sofa.Core.Node.addObject = myAddObject


def myAdd(self : Sofa.Core.Node, c, params = PrefabParameters(), **kwargs):  
    params = copy.copy(params)

    def findName(cname, node):
        """Compute a working unique name in the node"""
        rname = cname 
        for i in range(0, len(node.children)):
            if rname not in node.children:
                return rname
            rname = cname + str(i+1)
        return rname

    for k,v in kwargs.items():
        if hasattr(params, k):
            g = getattr(params,k)
            if isinstance(g, dict): 
                setattr(params, k, g | v)
            else:
                setattr(params, k, v)
                
    if params.name in self.children:
        params.name = findName(params.name, self)

    return c(parent = self, parameters=params) 
Sofa.Core.Node.add = myAdd

def createScene(root):
    #@optionalkwargs

    #def eulalieAddOde(self, **kwargs):
    #    self.addObject("EulerExplicitSolver", name="numericalintegration")
    #    self.addObject("LinearSolver", name="numericalsolver", firstOrder=True) 

    params = EntityParameters()
    params.mechanical.template = "Rigid3"
    params.mechanical.kwargs = { "showObject" : True, 
                                 "showObjectScale" : 10.0 }

    params.visual.geometry = GeometryFromFileParameters(filename="mesh/sphere_02.obj")
    params.addSimulation = entity.NONE
    
    root.add(Entity, name = "test", params=params)
    # root.add(Entity, name = "NoHide", mechanical = {"kwargs" : {"showObject":False }}, params=params)
    #root.add(Entity, params)

    #params.simulation.iterations = 10
    #params.simulation.integration["rayleighStiffness"] = 2.0
    #params.simulation.integration["rayleightStiffnessXXX"] = 2.0
    #params.solver.kwargs["numericalintegration"] = { "firstOrder" : True }

    root.add(Simulation, name="mySimulation")