from abaqusConstants import *
from .GeometricRestriction import GeometricRestriction
from ..Region.Region import Region


class ShapeMemberSize(GeometricRestriction):
    """The ShapeMemberSize object defines a shape member size geometric restriction.
    The ShapeMemberSize object is derived from the GeometricRestriction object. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import optimization
        mdb.models[name].optimizationTasks[name].geometricRestrictions[name]

    """

    def __init__(self, name: str, region: Region, maxThickness: float = 0, minThickness: float = 0,
                 sizeRestriction: SymbolicConstant = MINIMUM, assignNodeGroupRegion: str = OFF,
                 nodeGroupRegion: str = ''):
        """This method creates a ShapeMemberSize object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

                      mdb.models[name].optimizationTasks[name].ShapeMemberSize
        
        Parameters
        ----------
        name
            A String specifying the geometric restriction repository key. 
        region
            A Region object specifying the region to which the geometric restriction is applied. 
            When used with a TopologyTask, there is no default value. When used with a ShapeTask, 
            the default value is MODEL. 
        maxThickness
            A Float specifying the maximum thickness. The default value is 0.0. 
        minThickness
            A Float specifying the minimum thickness. The default value is 0.0. 
        sizeRestriction
            A SymbolicConstant specifying whether to restrict the minimum or maximum thickness. 
            Possible values are MAXIMUM and MINIMUM. The default value is MINIMUM. 
        assignNodeGroupRegion
            A bool specifying whether to use the node group region. The default value is OFF. 
        nodeGroupRegion
            A Node Region object specifying the check node group. 

        Returns
        -------
            A ShapeMemberSize object.
        """
        super().__init__()
        pass

    def setValues(self, maxThickness: float = 0, minThickness: float = 0,
                  sizeRestriction: SymbolicConstant = MINIMUM, assignNodeGroupRegion: str = OFF,
                  nodeGroupRegion: str = ''):
        """This method modifies the ShapeMemberSize object.
        
        Parameters
        ----------
        maxThickness
            A Float specifying the maximum thickness. The default value is 0.0. 
        minThickness
            A Float specifying the minimum thickness. The default value is 0.0. 
        sizeRestriction
            A SymbolicConstant specifying whether to restrict the minimum or maximum thickness. 
            Possible values are MAXIMUM and MINIMUM. The default value is MINIMUM. 
        assignNodeGroupRegion
            A bool specifying whether to use the node group region. The default value is OFF. 
        nodeGroupRegion
            A Node Region object specifying the check node group. 
        """
        pass
