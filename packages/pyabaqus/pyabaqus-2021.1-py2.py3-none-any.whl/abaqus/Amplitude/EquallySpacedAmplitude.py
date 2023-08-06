import typing

from abaqusConstants import *
from .Amplitude import Amplitude
from .BaselineCorrection import BaselineCorrection


class EquallySpacedAmplitude(Amplitude):
    """The EquallySpacedAmplitude object defines a list of amplitude values at fixed time
    intervals beginning at a specified value of time. 
    The EquallySpacedAmplitude object is derived from the Amplitude object. 

    Attributes
    ----------
    baselineCorrection: BaselineCorrection
        A :py:class:`~abaqus.Amplitude.BaselineCorrection.BaselineCorrection` object.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import amplitude
        mdb.models[name].amplitudes[name]
        import odbAmplitude
        session.odbs[name].amplitudes[name]

    The corresponding analysis keywords are:

    - AMPLITUDE

    """

    # A BaselineCorrection object. 
    baselineCorrection: BaselineCorrection = BaselineCorrection()

    def __init__(self, name: str, fixedInterval: float, data: tuple, begin: float = 0,
                 smooth: typing.Union[SymbolicConstant, float] = SOLVER_DEFAULT,
                 timeSpan: SymbolicConstant = STEP):
        """This method creates an EquallySpacedAmplitude object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].EquallySpacedAmplitude
            session.odbs[name].EquallySpacedAmplitude
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        fixedInterval
            A Float specifying the fixed time interval at which the amplitude data are given. 
            Possible values are positive numbers. 
        data
            A sequence of Floats specifying the amplitude values. 
        begin
            A Float specifying the time at which the first amplitude data are given. Possible values 
            are non-negative numbers. The default value is 0.0. 
        smooth
            The SymbolicConstant SOLVER_DEFAULT or a Float specifying the degree of smoothing. 
            Possible float values are 0 ≤≤ *smoothing* ≤≤ 0.5. If *smooth*=SOLVER_DEFAULT, the 
            default degree of smoothing will be determined by the solver. The default value is 
            SOLVER_DEFAULT. 
        timeSpan
            A SymbolicConstant specifying the time span of the amplitude. Possible values are STEP 
            and TOTAL. The default value is STEP. 

        Returns
        -------
            An EquallySpacedAmplitude object. 
            
        Raises
        ------
        InvalidNameError
        RangeError 
        """
        super().__init__()
        pass

    def setValues(self, begin: float = 0, smooth: typing.Union[SymbolicConstant, float] = SOLVER_DEFAULT,
                  timeSpan: SymbolicConstant = STEP):
        """This method modifies the EquallySpacedAmplitude object.
        
        Parameters
        ----------
        begin
            A Float specifying the time at which the first amplitude data are given. Possible values 
            are non-negative numbers. The default value is 0.0. 
        smooth
            The SymbolicConstant SOLVER_DEFAULT or a Float specifying the degree of smoothing. 
            Possible float values are 0 ≤≤ *smoothing* ≤≤ 0.5. If *smooth*=SOLVER_DEFAULT, the 
            default degree of smoothing will be determined by the solver. The default value is 
            SOLVER_DEFAULT. 
        timeSpan
            A SymbolicConstant specifying the time span of the amplitude. Possible values are STEP 
            and TOTAL. The default value is STEP.

        Raises
        ------
        RangeError
        """
        pass
