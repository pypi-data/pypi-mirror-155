from .GeometricRestriction import GeometricRestriction
from ..Region.Region import Region


class BeadPenetrationCheck(GeometricRestriction):
    """The BeadPenetrationCheck object defines a penetration check geometric restriction.
    The BeadPenetrationCheck object is derived from the GeometricRestriction object. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import optimization
        mdb.models[name].optimizationTasks[name].geometricRestrictions[name]

    """

    def __init__(self, name: str, beadPenetrationCheckRegion: Region, region: Region):
        """This method creates a BeadPenetrationCheck object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

                      mdb.models[name].optimizationTasks[name].BeadPenetrationCheck
        
        Parameters
        ----------
        name
            A String specifying the geometric restriction repository key. 
        beadPenetrationCheckRegion
            A Region object specifying the penetration check region. 
        region
            A Region object specifying the region to which the geometric restriction is applied. 

        Returns
        -------
            A BeadPenetrationCheck object.
        """
        super().__init__()
        pass

    def setValues(self):
        """This method modifies the BeadPenetrationCheck object.
        """
        pass
