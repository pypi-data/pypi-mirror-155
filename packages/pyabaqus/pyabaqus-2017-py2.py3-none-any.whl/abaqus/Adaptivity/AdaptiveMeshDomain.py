from ..Region.Region import Region


class AdaptiveMeshDomain:
    """The AdaptiveMeshDomain object defines the region and controls that govern an Arbitrary
    Lagrangian Eularian (ALE) style adaptive smoothing mesh domain. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import step
        mdb.models[name].steps[name].adaptiveMeshDomains[name]

    """

    def __init__(self, region: Region, controls: str = '', frequency: int = 10, initialMeshSweeps: int = 5,
                 meshSweeps: int = 1):
        """This method creates an AdaptiveMeshDomain object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].steps[name].AdaptiveMeshDomain
        
        Parameters
        ----------
        region
            A Region object specifying the region to which the adaptive mesh domain is applied. 
        controls
            A String specifying the name of an AdaptiveMeshControl object. 
        frequency
            An Int specifying the frequency in increments at which adaptive meshing will be 
            performed. The default value is 10. 
        initialMeshSweeps
            An Int specifying the number of mesh sweeps to be performed at the beginning of the 
            first step in which this adaptive mesh definition is active. The default value is 5. 
        meshSweeps
            An Int specifying the number of mesh sweeps to be performed in each adaptive mesh 
            increment. The default value is 1. 

        Returns
        -------
            An AdaptiveMeshDomain object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the AdaptiveMeshDomain object.

        Raises
        ------
        RangeError
        """
        pass
