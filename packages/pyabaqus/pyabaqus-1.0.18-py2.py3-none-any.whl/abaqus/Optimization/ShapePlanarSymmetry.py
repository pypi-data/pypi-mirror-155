from abaqusConstants import *
from .GeometricRestriction import GeometricRestriction
from ..Region.Region import Region


class ShapePlanarSymmetry(GeometricRestriction):
    """The ShapePlanarSymmetry object defines a shape planar symmetry geometric restriction.
    The ShapePlanarSymmetry object is derived from the GeometricRestriction object. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import optimization
        mdb.models[name].optimizationTasks[name].geometricRestrictions[name]

    """

    def __init__(self, name: str, clientDirection: tuple, region: Region,
                 allowNonSymmetricMesh: Boolean = TRUE, csys: int = None,
                 mainPointDetermination: SymbolicConstant = MAXIMUM,
                 presumeFeasibleRegionAtStart: Boolean = ON, tolerance1: float = 0,
                 tolerance2: float = 0, tolerance3: float = 0):
        """This method creates a ShapePlanarSymmetry object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

                      mdb.models[name].optimizationTasks[name].ShapePlanarSymmetry
        
        Parameters
        ----------
        name
            A String specifying the geometric restriction repository key. 
        clientDirection
            A VertexArray object of length 2 specifying the vector positioned at the *csys* origin 
            that is normal to the symmetry plane. Instead of through a ConstrainedSketchVertex, each point may be
            specified through a tuple of coordinates. 
        region
            A Region object specifying the region to which the geometric restriction is applied. 
            When used with a TopologyTask, there is no default value. When used with a ShapeTask, 
            the default value is MODEL. 
        allowNonSymmetricMesh
            A Boolean specifying whether to allow a nonsymmetric mesh for this geometric 
            restriction. The default value is TRUE. 
        csys
            None or a DatumCsys object specifying the local coordinate system. If *csys*=None, the 
            global coordinate system is used. When this member is queried, it returns an Int. The 
            default value is None. 
        mainPointDetermination
            A SymbolicConstant specifying the rule for determining the main node. Possible values 
            are MAXIMUM and MINIMUM. The default value is MAXIMUM. 
        presumeFeasibleRegionAtStart
            A Boolean specifying whether to ignore the geometric restriction in the first design 
            cycle. The default value is ON. 
        tolerance1
            A Float specifying the geometric tolerance in the 1-direction. The default value is 
            0.01. 
        tolerance2
            A Float specifying the geometric tolerance in the 2-direction. The default value is 
            0.01. 
        tolerance3
            A Float specifying the geometric tolerance in the 3-direction. The default value is 
            0.01. 

        Returns
        -------
            A ShapePlanarSymmetry object.
        """
        super().__init__()
        pass

    def setValues(self, allowNonSymmetricMesh: Boolean = TRUE, csys: int = None,
                  mainPointDetermination: SymbolicConstant = MAXIMUM,
                  presumeFeasibleRegionAtStart: Boolean = ON, tolerance1: float = 0,
                  tolerance2: float = 0, tolerance3: float = 0):
        """This method modifies the ShapePlanarSymmetry object.
        
        Parameters
        ----------
        allowNonSymmetricMesh
            A Boolean specifying whether to allow a nonsymmetric mesh for this geometric 
            restriction. The default value is TRUE. 
        csys
            None or a DatumCsys object specifying the local coordinate system. If *csys*=None, the 
            global coordinate system is used. When this member is queried, it returns an Int. The 
            default value is None. 
        mainPointDetermination
            A SymbolicConstant specifying the rule for determining the main node. Possible values 
            are MAXIMUM and MINIMUM. The default value is MAXIMUM. 
        presumeFeasibleRegionAtStart
            A Boolean specifying whether to ignore the geometric restriction in the first design 
            cycle. The default value is ON. 
        tolerance1
            A Float specifying the geometric tolerance in the 1-direction. The default value is 
            0.01. 
        tolerance2
            A Float specifying the geometric tolerance in the 2-direction. The default value is 
            0.01. 
        tolerance3
            A Float specifying the geometric tolerance in the 3-direction. The default value is 
            0.01. 
        """
        pass
