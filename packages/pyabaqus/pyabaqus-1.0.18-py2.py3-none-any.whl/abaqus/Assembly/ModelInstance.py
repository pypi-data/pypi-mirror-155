from abaqusConstants import *
from ..BasicGeometry.EdgeArray import EdgeArray
from ..BasicGeometry.ReferencePoint import ReferencePoint
from ..BasicGeometry.VertexArray import VertexArray
from ..Datum.Datum import Datum
from ..Mesh.MeshElementArray import MeshElementArray
from ..Mesh.MeshNodeArray import MeshNodeArray
# from ..Model.Model import Model
from ..Region.Set import Set
from ..Region.Surface import Surface


# prevent circular imports
class Model:
    pass


class ModelInstance:
    """A ModelInstance object is an instance of a Model.

    Attributes
    ----------
    sets: dict[str, Set]
        A repository of :py:class:`~abaqus.Region.Set.Set` objects specifying the sets created on the assembly. For more
        information, see [Region
        commands](https://help.3ds.com/2022/english/DSSIMULIA_Established/SIMACAEKERRefMap/simaker-m-RegPyc-sb.htm?ContextScope=all).
    surfaces: dict[str, Surface]
        A repository of :py:class:`~abaqus.Region.Surface.Surface` objects specifying the surfaces created on the assembly. For
        more information, see [Region
        commands](https://help.3ds.com/2022/english/DSSIMULIA_Established/SIMACAEKERRefMap/simaker-m-RegPyc-sb.htm?ContextScope=all).
    vertices: VertexArray
        A :py:class:`~abaqus.BasicGeometry.VertexArray.VertexArray` object.
    edges: EdgeArray
        An :py:class:`~abaqus.BasicGeometry.EdgeArray.EdgeArray` object.
    elements: MeshElementArray
        A :py:class:`~abaqus.Mesh.MeshElementArray.MeshElementArray` object.
    nodes: MeshNodeArray
        A :py:class:`~abaqus.Mesh.MeshNodeArray.MeshNodeArray` object.
    datums: dict[str, Datum]
        A repository of :py:class:`~abaqus.Datum.Datum.Datum` objects.
    referencePoints: dict[str, ReferencePoint]
        A repository of :py:class:`~abaqus.BasicGeometry.ReferencePoint.ReferencePoint` objects.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import assembly
        mdb.models[name].rootAssembly.modelInstances[i]

    """

    # A repository of Set objects specifying the sets created on the assembly. For more 
    # information, see [Region 
    # commands](https://help.3ds.com/2022/english/DSSIMULIA_Established/SIMACAEKERRefMap/simaker-m-RegPyc-sb.htm?ContextScope=all). 
    sets: dict[str, Set] = dict[str, Set]()

    # A repository of Surface objects specifying the surfaces created on the assembly. For 
    # more information, see [Region 
    # commands](https://help.3ds.com/2022/english/DSSIMULIA_Established/SIMACAEKERRefMap/simaker-m-RegPyc-sb.htm?ContextScope=all). 
    surfaces: dict[str, Surface] = dict[str, Surface]()

    # A VertexArray object. 
    vertices: VertexArray = VertexArray([])

    # An EdgeArray object. 
    edges: EdgeArray = EdgeArray([])

    # A MeshElementArray object. 
    elements: MeshElementArray = MeshElementArray([])

    # A MeshNodeArray object. 
    nodes: MeshNodeArray = MeshNodeArray([])

    # A repository of Datum objects. 
    datums: dict[str, Datum] = dict[str, Datum]()

    # A repository of ReferencePoint objects. 
    referencePoints: dict[str, ReferencePoint] = dict[str, ReferencePoint]()

    def __init__(self, name: str, model: Model, autoOffset: Boolean = OFF):
        """This method creates a ModelInstance object and puts it into the instances repository.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].rootAssembly.Instance
        
        Parameters
        ----------
        name
            The repository key. The name must be a valid Abaqus object name. 
        model
            A Model object to be instanced. If the model does not exist, no ModelInstance object is 
            created. 
        autoOffset
            A Boolean specifying whether to apply an auto offset to the new instance that will 
            offset it from existing instances. The default value is OFF. 

        Returns
        -------
            A ModelInstance object.
        """
        pass

    def ConvertConstraints(self):
        """This method converts the position constraints of an instance to absolute positions. The
        method deletes the constraint features on the instance but preserves the position in
        space.
        """
        pass

    def getPosition(self):
        """This method prints the sum of the translations and rotations applied to the
        ModelInstance object.
        """
        pass

    def replace(self, instanceOf: Model, applyConstraints: Boolean = True):
        """This method replaces one instance with an instance of another model.
        
        Parameters
        ----------
        instanceOf
            A Model object to be instanced. If the model does not exist, no ModelInstance object is 
            created. 
        applyConstraints
            A Boolean specifying whether to apply existing constraints on the new instance or to 
            position the new instance in the same place as the original instance. The default value 
            is True. A value of False indicates that constraints applies to the instance are deleted 
            will be deleted from the feature list. 
        """
        pass

    def translate(self, vector: tuple):
        """This method translates an instance by the specified amount.
        
        Parameters
        ----------
        vector
            A sequence of three Floats specifying a translation vector. 
        """
        pass
