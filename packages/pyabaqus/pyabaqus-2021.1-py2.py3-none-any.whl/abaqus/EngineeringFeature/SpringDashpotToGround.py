from abaqusConstants import *
from .SpringDashpot import SpringDashpot
from ..Region.Region import Region


class SpringDashpotToGround(SpringDashpot):
    """The SpringDashpotToGround object defines springs and/or dashpots between points and
    ground on a part or an assembly region. 
    The SpringDashpotToGround object is derived from the SpringDashpot object. 

    Attributes
    ----------
    suppressed: Boolean
        A Boolean specifying whether the spring/dashpot is suppressed or not. The default value
        is OFF.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import part
        mdb.models[name].parts[name].engineeringFeatures.springDashpots[name]
        import assembly
        mdb.models[name].rootAssembly.engineeringFeatures.springDashpots[name]

    The corresponding analysis keywords are:

    - ELEMENT
            - SPRING
            - DASHPOT

    """

    # A Boolean specifying whether the spring/dashpot is suppressed or not. The default value 
    # is OFF. 
    suppressed: Boolean = OFF

    def __init__(self, name: str, region: Region, dof: int, orientation: str = None,
                 springBehavior: Boolean = OFF, dashpotBehavior: Boolean = OFF,
                 springStiffness: float = 0, dashpotCoefficient: float = 0):
        """This method creates a SpringDashpotToGround object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].parts[name].engineeringFeatures.SpringDashpotToGround
            mdb.models[name].rootAssembly.engineeringFeatures\
            .SpringDashpotToGround
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        region
            A Region object specifying the region to which the springs and/or dashpots are applied. 
        dof
            An Int specifying the degree of freedom associated with the spring and dashpot 
            behaviors. 
        orientation
            None or a DatumCsys object specifying the local directions for the spring and/or 
            dashpot. If *orientation*=None, the spring and/or dashpot data are defined in the global 
            coordinate system. The default value is None. 
        springBehavior
            A Boolean specifying whether to apply spring behavior to the selected points. The 
            default value is OFF.At least one of the arguments *springBehavior*=ON or 
            *dashpotBehavior*=ON must be specified. 
        dashpotBehavior
            A Boolean specifying whether to apply dashpot behavior to the selected points. The 
            default value is OFF.At least one of the arguments *springBehavior*=ON or 
            *dashpotBehavior*=ON must be specified. 
        springStiffness
            A Float specifying the force per relative displacement for the spring. The default value 
            is 0.0. 
        dashpotCoefficient
            A Float specifying the force per relative velocity for the dashpot. The default value is 
            0.0. 

        Returns
        -------
            A SpringDashpotToGround object.
        """
        super().__init__()
        pass

    def setValues(self, orientation: str = None, springBehavior: Boolean = OFF, dashpotBehavior: Boolean = OFF,
                  springStiffness: float = 0, dashpotCoefficient: float = 0):
        """This method modifies the SpringDashpotToGround object.
        
        Parameters
        ----------
        orientation
            None or a DatumCsys object specifying the local directions for the spring and/or 
            dashpot. If *orientation*=None, the spring and/or dashpot data are defined in the global 
            coordinate system. The default value is None. 
        springBehavior
            A Boolean specifying whether to apply spring behavior to the selected points. The 
            default value is OFF.At least one of the arguments *springBehavior*=ON or 
            *dashpotBehavior*=ON must be specified. 
        dashpotBehavior
            A Boolean specifying whether to apply dashpot behavior to the selected points. The 
            default value is OFF.At least one of the arguments *springBehavior*=ON or 
            *dashpotBehavior*=ON must be specified. 
        springStiffness
            A Float specifying the force per relative displacement for the spring. The default value 
            is 0.0. 
        dashpotCoefficient
            A Float specifying the force per relative velocity for the dashpot. The default value is 
            0.0. 
        """
        pass
