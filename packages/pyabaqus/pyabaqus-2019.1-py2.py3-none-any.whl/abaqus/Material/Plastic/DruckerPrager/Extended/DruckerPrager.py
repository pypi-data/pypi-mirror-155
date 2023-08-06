from abaqusConstants import *
from .DruckerPragerCreep import DruckerPragerCreep
from .DruckerPragerHardening import DruckerPragerHardening
from .TriaxialTestData import TriaxialTestData
from ...Metal.RateDependent.RateDependent import RateDependent


class DruckerPrager:
    """The DruckerPrager object specifies the extended Drucker-Prager plasticity model.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import material
        mdb.models[name].materials[name].druckerPrager
        import odbMaterial
        session.odbs[name].materials[name].druckerPrager

    The table data for this object are:

    - If *shearCriterion*=LINEAR (the only option allowed in an Abaqus/Explicit analysis), the table data specify the following:
        - Material angle of friction, β, in the p–t plane. Give the value in degrees.
        - K, the ratio of the flow stress in triaxial tension to the flow stress in triaxial compression. 0.778≤K≤1.0.
            If the default value of 0.0 is accepted, a value of 1.0 is assumed.
        - Dilation angle, ψ, in the p–t plane. Give the value in degrees.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.
    - If *shearCriterion*=HYPERBOLIC, the table data specify the following:
        - Material angle of friction, β, at high confining pressure in the p–q plane. Give the value in degrees.
        - Initial hydrostatic tension strength, pt|0.
        - Dilation angle, ψ, at high confining pressure in the p–q plane. Give the value in degrees.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.
    - If *shearCriterion*=EXPONENTIAL, the table data specify the following:
        - Dilation angle, ψ, at high confining pressure in the p–q plane. Give the value in degrees.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.

    The corresponding analysis keywords are:

    - DRUCKER PRAGER

    """

    # A DruckerPragerCreep object. 
    druckerPragerCreep: DruckerPragerCreep = DruckerPragerCreep(((),))

    # A DruckerPragerHardening object. 
    druckerPragerHardening: DruckerPragerHardening = DruckerPragerHardening(((),))

    # A RateDependent object. 
    rateDependent: RateDependent = RateDependent(((),))

    # A TriaxialTestData object. 
    triaxialTestData: TriaxialTestData = TriaxialTestData(((),))

    def __init__(self, table: tuple, shearCriterion: SymbolicConstant = LINEAR, eccentricity: float = 0,
                 testData: Boolean = OFF, temperatureDependency: Boolean = OFF, dependencies: int = 0):
        """This method creates a DruckerPrager object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].DruckerPrager
                session.odbs[name].materials[name].DruckerPrager
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        shearCriterion
            A SymbolicConstant specifying the yield criterion. Possible values are LINEAR, 
            HYPERBOLIC, and EXPONENTIAL. The default value is LINEAR.This argument applies only to 
            Abaqus/Standard analyses. Only the linear Drucker-Prager model is available in 
            Abaqus/Explicit analyses. 
        eccentricity
            A Float specifying the flow potential eccentricity, ϵϵ, a small positive number that 
            defines the rate at which the hyperbolic flow potential approaches its asymptote. The 
            default value is 0.1.This argument applies only to Abaqus/Standard analyses. 
        testData
            A Boolean specifying whether the material constants for the exponent model are to be 
            computed by Abaqus/Standard from triaxial test data at different levels of confining 
            pressure. The default value is OFF.This argument is valid only if 
            *shearCriterion*=EXPONENTIAL. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A DruckerPrager object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the DruckerPrager object.

        Raises
        ------
        RangeError
        """
        pass
