from abaqusConstants import *
from .Metal.Annealing.AnnealTemperature import AnnealTemperature
from .Metal.Cyclic.CycledPlastic import CycledPlastic
from .Metal.Cyclic.CyclicHardening import CyclicHardening
from .Metal.ORNL.Ornl import Ornl
from .Metal.RateDependent.RateDependent import RateDependent
from .Potential import Potential
from .TensileFailure import TensileFailure


class Plastic:
    """The Plastic object specifies a metal plasticity model.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import material
        mdb.models[name].materials[name].Plastic
        import odbMaterial
        session.odbs[name].materials[name].Plastic

    The table data for this object are:
    
    - If *hardening*=ISOTROPIC, or if *hardening*=COMBINED and *dataType*=HALF_CYCLE, the table data specify the following:
        - Yield stress.
        - Plastic strain.
        - Equivalent Plastic strain rate, ε¯˙p⁢l.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.
    - If *hardening*=COMBINED and *dataType*=STABILIZED, the table data specify the following:
        - Yield stress.
        - Plastic strain.
        - Strain range, if the data depend on strain range.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.
    - If *hardening*=COMBINED and *dataType*=PARAMETERS, the table data specify the following:
        - Yield stress at zero Plastic strain.
        - The first kinematic hardening parameter, C1.
        - The first kinematic hardening parameter, γ1.
        - If applicable, the second kinematic hardening parameter, C2.
        - If applicable, the second kinematic hardening parameter, γ2.
        - Etc.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.
    - If *hardening*=KINEMATIC, the table data specify the following:
        - Yield stress.
        - Plastic strain.
        - Temperature, if the data depend on temperature.
    - If *hardening*=JOHNSON_COOK, the table data specify the following:
        - A.
        - B.
        - n.
        - m.
        - Melting temperature.
        - Transition temperature.
    - If *hardening*=USER, the table data specify the following:
        - Hardening properties.

    The corresponding analysis keywords are:

    - PLASTIC

    """

    # A RateDependent object. 
    rateDependent: RateDependent = RateDependent(((),))

    # A Potential object. 
    potential: Potential = Potential(((),))

    # A CyclicHardening object. 
    cyclicHardening: CyclicHardening = CyclicHardening(((),))

    # An Ornl object. 
    ornl: Ornl = Ornl()

    # A CycledPlastic object. 
    cycledPlastic: CycledPlastic = CycledPlastic(((),))

    # An AnnealTemperature object. 
    annealTemperature: AnnealTemperature = AnnealTemperature(((),))

    # A TensileFailure object. 
    tensileFailure: TensileFailure = TensileFailure()

    def __init__(self, table: tuple, hardening: SymbolicConstant = ISOTROPIC, rate: Boolean = OFF,
                 dataType: SymbolicConstant = HALF_CYCLE, strainRangeDependency: Boolean = OFF,
                 numBackstresses: int = 1, temperatureDependency: Boolean = OFF, dependencies: int = 0):
        """This method creates a Plastic object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Plastic
                session.odbs[name].materials[name].Plastic
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        hardening
            A SymbolicConstant specifying the type of hardening. Possible values are ISOTROPIC, 
            KINEMATIC, COMBINED, JOHNSON_COOK, and USER. The default value is ISOTROPIC. 
        rate
            A Boolean specifying whether the data depend on rate. The default value is OFF. 
        dataType
            A SymbolicConstant specifying the type of combined hardening. This argument is only 
            valid if *hardening*=COMBINED. Possible values are HALF_CYCLE, PARAMETERS, and 
            STABILIZED. The default value is HALF_CYCLE. 
        strainRangeDependency
            A Boolean specifying whether the data depend on strain range. This argument is only 
            valid if *hardening*=COMBINED and *dataType*=STABILIZED. The default value is OFF. 
        numBackstresses
            An Int specifying the number of backstresses. This argument is only valid if 
            *hardening*=COMBINED. The default value is 1. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A Plastic object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the Plastic object.

        Raises
        ------
        RangeError
        """
        pass
