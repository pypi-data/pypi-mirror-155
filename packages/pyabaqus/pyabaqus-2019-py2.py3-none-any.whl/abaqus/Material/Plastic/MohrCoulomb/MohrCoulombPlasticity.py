from abaqusConstants import *
from .MohrCoulombHardening import MohrCoulombHardening
from .TensionCutOff import TensionCutOff


class MohrCoulombPlasticity:
    """The MohrCoulombPlasticity object specifies the extended Mohr-Coulomb plasticity model.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import material
        mdb.models[name].materials[name].mohrCoulombPlasticity
        import odbMaterial
        session.odbs[name].materials[name].mohrCoulombPlasticity

    The table data for this object are:

    - Friction angle (given in degrees), ϕ, at high confining pressure in the p–Rm⁢c⁢q plane.
    - Dilation angle, ψ, at high confining pressure in the p–Rm⁢w⁢q plane.
    - Temperature, if the data depend on temperature.
    - Value of the first field variable, if the data depend on field variables.
    - Value of the second field variable.
    - Etc.

    The corresponding analysis keywords are:

    - MOHR COULOMB

    """

    # A MohrCoulombHardening object. 
    mohrCoulombHardening: MohrCoulombHardening = MohrCoulombHardening(((),))

    # A TensionCutOff object. 
    tensionCutOff: TensionCutOff = TensionCutOff(((),))

    def __init__(self, table: tuple, deviatoricEccentricity: float = None, meridionalEccentricity: float = 0,
                 temperatureDependency: Boolean = OFF, dependencies: int = 0,
                 useTensionCutoff: Boolean = OFF):
        """This method creates a MohrCoulombPlasticity object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].MohrCoulombPlasticity
                session.odbs[name].materials[name].MohrCoulombPlasticity
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        deviatoricEccentricity
            None or a Float specifying the flow potential eccentricity in the deviatoric plane, e; 
            1/2 ≤ 1.0. If *deviatoricEccentricity*=None, Abaqus calculates the value using the 
            specified Mohr-Coulomb angle of friction. The default value is None. 
        meridionalEccentricity
            A Float specifying the flow potential eccentricity in the meridional plane, ϵϵ. The 
            default value is 0.1. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 
        useTensionCutoff
            A Boolean specifying whether tension cutoff specification is needed. The default value 
            is OFF. 

        Returns
        -------
            A MohrCoulombPlasticity object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the MohrCoulombPlasticity object.

        Raises
        ------
        RangeError
        """
        pass
