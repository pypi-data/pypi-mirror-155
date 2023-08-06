from abaqusConstants import *
from .Crack import Crack


class DebondVCCT(Crack):
    """The DebondVCCT object defines the parameters needed to activate crack propagation using
    VCCT. 
    The DebondVCCT object is derived from the Crack object. 

    Attributes
    ----------
    suppressed: Boolean
        A Boolean specifying whether the crack is suppressed or not. The default value is OFF.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import part
        mdb.models[name].parts[name].engineeringFeatures.cracks[name]
        import assembly
        mdb.models[name].rootAssembly.engineeringFeatures.cracks[name]

    The corresponding analysis keywords are:

    - DEBOND

    """

    # A Boolean specifying whether the crack is suppressed or not. The default value is OFF. 
    suppressed: Boolean = OFF

    def __init__(self, name: str, initiationStep: str, surfToSurfInteraction: str,
                 debondingForceAmplitude: SymbolicConstant = STEP, printToDATFrequency: int = 1):
        """This method creates a DebondVCCT object. Although the constructor is available both for
        parts and for the assembly, DebondVCCT objects are currently supported only under the
        assembly.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].parts[name].engineeringFeatures.DebondVCCT
            mdb.models[name].rootAssembly.engineeringFeatures.DebondVCCT
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        initiationStep
            A String specifying the name of the step in which the DebondVCCT object is created. 
        surfToSurfInteraction
            A String specifying the name of the SurfaceToSurfaceContactStd object that defines the 
            surface to surface interaction for the crack surfaces. 
        debondingForceAmplitude
            A SymbolicConstant specifying whether the debond force between the two surfaces at the 
            crack tip is to be released immediately or gradually during the following increment 
            after debonding. Possible values are STEP and RAMP. The default value is STEP. 
        printToDATFrequency
            An Int specifying the frequency at which output will be printed to DAT file. The default 
            value is 1. 

        Returns
        -------
            A DebondVCCT object.
        """
        super().__init__()
        pass

    def setValues(self, debondingForceAmplitude: SymbolicConstant = STEP, printToDATFrequency: int = 1):
        """This method modifies the DebondVCCT object.
        
        Parameters
        ----------
        debondingForceAmplitude
            A SymbolicConstant specifying whether the debond force between the two surfaces at the 
            crack tip is to be released immediately or gradually during the following increment 
            after debonding. Possible values are STEP and RAMP. The default value is STEP. 
        printToDATFrequency
            An Int specifying the frequency at which output will be printed to DAT file. The default 
            value is 1. 
        """
        pass
