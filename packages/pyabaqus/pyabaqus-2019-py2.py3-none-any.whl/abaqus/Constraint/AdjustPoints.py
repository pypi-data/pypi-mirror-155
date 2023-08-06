from abaqusConstants import *
from .Constraint import Constraint
from ..Region.Region import Region


class AdjustPoints(Constraint):
    """The AdjustPoints constraint object is used to adjust points (nodes) to a surface.
    The AdjustPoints object is derived from the ConstrainedSketchConstraint object.

    Attributes
    ----------
    suppressed: Boolean
        A Boolean specifying whether the constraint is suppressed or not. The default value is
        OFF.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import interaction
        mdb.models[name].constraints[name]

    The corresponding analysis keywords are:

    - ADJUST

    """

    # A Boolean specifying whether the constraint is suppressed or not. The default value is 
    # OFF. 
    suppressed: Boolean = OFF

    def __init__(self, name: str, surface: Region, controlPoints: Region):
        """This method creates an AdjustPoints object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].AdjustPoints
        
        Parameters
        ----------
        name
            A String specifying the constraint repository key. 
        surface
            A Region object specifying the surface to which the *controlPoints* are adjusted. 
        controlPoints
            A Region object specifying the constraint control points. 

        Returns
        -------
            An AdjustPoints object.
        """
        super().__init__()
        pass

    def setValues(self):
        """This method modifies the AdjustPoints object.
        """
        pass
