from abaqusConstants import *


class StopCondition:
    """The StopCondition object is the abstract base type for other StopCondition objects. The
    StopCondition object has no explicit constructor. The methods and members of the 
    StopCondition object are common to all objects derived from StopCondition. 

    Attributes
    ----------
    name: str
        A String specifying the stop condition repository key.
    region: SymbolicConstant
        The SymbolicConstant MODEL or a :py:class:`~abaqus.Region.Region.Region` object specifying the region to which the stop
        condition is applied. The default value is MODEL.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import optimization
        mdb.models[name].optimizationTasks[name].stopConditions[name]

    """

    # A String specifying the stop condition repository key. 
    name: str = ''

    # The SymbolicConstant MODEL or a Region object specifying the region to which the stop 
    # condition is applied. The default value is MODEL. 
    region: SymbolicConstant = MODEL
