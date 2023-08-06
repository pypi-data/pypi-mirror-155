from abaqusConstants import *


class CapCreepConsolidation:
    """The CapCreepConsolidation object specifies a cap creep model and material properties.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import material
        mdb.models[name].materials[name].capPlasticity.capCreepConsolidation
        import odbMaterial
        session.odbs[name].materials[name].capPlasticity.capCreepConsolidation

    The table data for this object are:

    - If *law*=STRAIN or *law*=TIME, the table data specify the following:
        - A.
        - n.
        - m.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.
    - If *law*=SINGHM, the table data specify the following:
        - A.
        - α.
        - m.
        - t1.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.
    - If *law*=POWER_LAW or *law*=TIME_POWER_LAW, the table data specify the following:
        - q0.
        - n.
        - m.
        - .ε0.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.

    The corresponding analysis keywords are:

    - CAP CREEP

    """

    def __init__(self, table: tuple, law: SymbolicConstant = STRAIN, temperatureDependency: Boolean = OFF,
                 dependencies: int = 0, time: SymbolicConstant = TOTAL):
        """This method creates a CapCreepConsolidation object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].capPlasticity.CapCreepConsolidation
                session.odbs[name].materials[name].capPlasticity.CapCreepConsolidation
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        law
            A SymbolicConstant specifying the cap creep law. Possible values are STRAIN, TIME, 
            SINGHM, and USER. The default value is STRAIN. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 
        time
            A SymbolicConstant specifying the time increment for the relevant laws. Possible values 
            are CREEP and TOTAL. The default value is TOTAL. 

        Returns
        -------
            A CapCreepConsolidation object.
        """
        pass

    def setValues(self):
        """This method modifies the CapCreepConsolidation object.
        """
        pass
