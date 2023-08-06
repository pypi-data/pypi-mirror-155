from abaqusConstants import *


class Expansion:
    """The Expansion object specifies thermal expansion.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import material
        mdb.models[name].materials[name].expansion
        import odbMaterial
        session.odbs[name].materials[name].expansion

    The table data for this object are:

    - If *type*=ISOTROPIC, the table data specify the following:
        - α in Abaqus/Standard or Abaqus/Explicit analysis.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.
    - If *type*=ORTHOTROPIC, the table data specify the following:
        - α11.
        - α22.
        - α33.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.
    - If *type*=ANISOTROPIC, the table data specify the following:
        - α11.
        - α22.
        - α33. (Not used for plane stress case.)
        - α12.
        - α13.
        - α23.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.
    - If *type*=SHORT_FIBER, there is no table data.

    The corresponding analysis keywords are:

    - EXPANSION

    """

    def __init__(self, type: SymbolicConstant = ISOTROPIC, userSubroutine: Boolean = OFF, zero: float = 0,
                 temperatureDependency: Boolean = OFF, dependencies: int = 0, table: tuple = ()):
        """This method creates an Expansion object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Expansion
                session.odbs[name].materials[name].Expansion
        
        Parameters
        ----------
        type
            A SymbolicConstant specifying the type of expansion. Possible values are ISOTROPIC, 
            ORTHOTROPIC, ANISOTROPIC, and SHORT_FIBER. The default value is ISOTROPIC. 
        userSubroutine
            A Boolean specifying whether a user subroutine is used to define the increments of 
            thermal strain. The default value is OFF. 
        zero
            A Float specifying the value of θ0 if the thermal expansion is temperature-dependent or 
            field-variable-dependent. The default value is 0.0. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 
        table
            A sequence of sequences of Floats specifying the items described below. The default 
            value is an empty sequence.This argument is required only if *type* is not USER. 

        Returns
        -------
            An Expansion object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the Expansion object.

        Raises
        ------
        RangeError
        """
        pass
