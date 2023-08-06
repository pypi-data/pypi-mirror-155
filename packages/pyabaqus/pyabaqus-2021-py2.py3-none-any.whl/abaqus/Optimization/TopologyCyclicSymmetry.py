from abaqusConstants import *
from .GeometricRestriction import GeometricRestriction
from ..Region.Region import Region


class TopologyCyclicSymmetry(GeometricRestriction):
    """The TopologyCyclicSymmetry object defines a topology cyclic symmetry geometric
    restriction. 
    The TopologyCyclicSymmetry object is derived from the GeometricRestriction object. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import optimization
        mdb.models[name].optimizationTasks[name].geometricRestrictions[name]

    """

    def __init__(self, name: str, region: Region, translation: float, axis: SymbolicConstant = AXIS_1,
                 csys: int = None, ignoreFrozenArea: Boolean = OFF):
        """This method creates a TopologyCyclicSymmetry object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

                      mdb.models[name].optimizationTasks[name].TopologyCyclicSymmetry
        
        Parameters
        ----------
        name
            A String specifying the geometric restriction repository key. 
        region
            A Region object specifying the region to which the geometric restriction is applied. 
            When used with a TopologyTask, there is no default value. When used with a ShapeTask, 
            the default value is MODEL. 
        translation
            A Float specifying the translation distance. 
        axis
            A SymbolicConstant specifying the translation direction defined along an axis positioned 
            at the *csys* origin. Possible values are AXIS_1, AXIS_2, and AXIS_3. The default value 
            is AXIS_1. 
        csys
            None or a DatumCsys object specifying the local coordinate system. If *csys*=None, the 
            global coordinate system is used. When this member is queried, it returns an Int. The 
            default value is None. 
        ignoreFrozenArea
            A Boolean specifying whether to ignore frozen areas. The default value is OFF. 

        Returns
        -------
            A TopologyCyclicSymmetry object.
        """
        super().__init__()
        pass

    def setValues(self, axis: SymbolicConstant = AXIS_1, csys: int = None, ignoreFrozenArea: Boolean = OFF):
        """This method modifies the TopologyCyclicSymmetry object.
        
        Parameters
        ----------
        axis
            A SymbolicConstant specifying the translation direction defined along an axis positioned 
            at the *csys* origin. Possible values are AXIS_1, AXIS_2, and AXIS_3. The default value 
            is AXIS_1. 
        csys
            None or a DatumCsys object specifying the local coordinate system. If *csys*=None, the 
            global coordinate system is used. When this member is queried, it returns an Int. The 
            default value is None. 
        ignoreFrozenArea
            A Boolean specifying whether to ignore frozen areas. The default value is OFF. 
        """
        pass
