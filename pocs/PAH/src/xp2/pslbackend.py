from pslir import IRNode, Prefab, Object

def serialize_object(ir: IRNode) -> str:
    if not isinstance(ir.type, type):  
        raise Exception("Invalid IRNode.type for an Object. It must be a string")
    return f"""self.addObject({str(ir.psl_instance)}, **kwargs)"""
    
def serialize_prefab(ir: IRNode) -> str:
    tmp = ""

    for entry in ir.children:
        tmp += serialize_entry(entry)
    
    return f""" 
def add_f{ir.name}(parent = None, **kwargs):
    if parent is not None:
        self = parent.addChild(**kwargs)
    else:
        self = Sofa.Core.Node(**kwargs)

    {tmp}
"""

def serialize_entry(ir: IRNode) -> str:
    """Dispatch the serialisation between Prefab and Object"""
    print(ir.type, Prefab)
    if ir.type == Prefab:
        return serialize_prefab(ir)
    elif ir.type == Object:
        return serialize_object(ir)
    raise Exception(f"IRNode type should be pslir.Prefab or pslir.Object, found {ir.type}")

def serialize(ir : IRNode) -> str:
    return serialize_entry(ir) 
