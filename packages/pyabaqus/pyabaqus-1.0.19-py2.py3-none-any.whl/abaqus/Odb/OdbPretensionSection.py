from .OdbMeshNode import OdbMeshNode
from .OdbSet import OdbSet


class OdbPretensionSection:
    """The pretension section object is used to define an assembly load. It associates a
    pretension node with a pretension section. 

    Attributes
    ----------
    node: OdbSet
        An :py:class:`~abaqus.Odb.OdbSet.OdbSet` object specifying the node set containing the pretension node.
    element: OdbSet
        An :py:class:`~abaqus.Odb.OdbSet.OdbSet` object specifying the element set that defines the pretension section.
    surface: OdbSet
        An :py:class:`~abaqus.Odb.OdbSet.OdbSet` object specifying the surface set that defines the pretension section.
    normal: float
        A tuple of Floats specifying the components of the normal to the pretension section.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import odbAccess
        session.odbs[name].rootAssembly.pretensionSections[i]

    """

    # An OdbSet object specifying the node set containing the pretension node. 
    node: OdbSet = OdbSet('set', tuple[OdbMeshNode]())

    # An OdbSet object specifying the element set that defines the pretension section. 
    element: OdbSet = OdbSet('set', tuple[OdbMeshNode]())

    # An OdbSet object specifying the surface set that defines the pretension section. 
    surface: OdbSet = OdbSet('set', tuple[OdbMeshNode]())

    # A tuple of Floats specifying the components of the normal to the pretension section. 
    normal: float = None
