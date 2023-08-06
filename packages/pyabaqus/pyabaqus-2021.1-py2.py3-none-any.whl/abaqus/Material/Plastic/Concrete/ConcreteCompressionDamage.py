from abaqusConstants import *


class ConcreteCompressionDamage:
    """The ConcreteCompressionDamage object specifies hardening for the concrete damaged
    plasticity model. 

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import material
        mdb.models[name].materials[name].concreteDamagedPlasticity.concreteCompressionDamage
        import odbMaterial
        session.odbs[name].materials[name].concreteDamagedPlasticity.concreteCompressionDamage

    The table data for this object are:

    - Compressive damage variable, dc.
    - Plastic (crushing) strain, ϵci⁢n.
    - Temperature, if the data depend on temperature.
    - Value of the first field variable, if the data depend on field variables.
    - Value of the second field variable.
    - Etc.

    The corresponding analysis keywords are:

    - CONCRETE COMPRESSION DAMAGE

    """

    def __init__(self, table: tuple, tensionRecovery: float = 0, temperatureDependency: Boolean = OFF,
                 dependencies: int = 0):
        """This method creates a ConcreteCompressionDamage object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].concreteDamagedPlasticity.ConcreteCompressionDamage
                session.odbs[name].materials[name].concreteDamagedPlasticity.ConcreteCompressionDamage
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        tensionRecovery
            A Float specifying the value of the stiffness recovery factor, wtwt, that determines the 
            amount of tension stiffness that is recovered as loading changes from compression to 
            tension. The default value is 0.0. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A ConcreteCompressionDamage object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the ConcreteCompressionDamage object.

        Raises
        ------
        RangeError
        """
        pass
