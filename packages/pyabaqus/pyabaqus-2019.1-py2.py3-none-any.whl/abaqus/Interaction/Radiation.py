

class Radiation:
    """The Radiation object specifies radiation for a contact interaction property.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import interaction
        mdb.models[name].interactionProperties[name].radiation

    The corresponding analysis keywords are:

    - GAP RADIATION

    """

    def __init__(self, mainEmissivity: float, secondaryEmissivity: float, table: tuple):
        """This method creates a Radiation object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].interactionProperties[name].Radiation
        
        Parameters
        ----------
        mainEmissivity
            A Float specifying the emissivity of the main surface. 
        secondaryEmissivity
            A Float specifying the emissivity of the secondary surface. 
        table
            A sequence of sequences of Floats specifying the following:Effective viewfactor, FF.Gap 
            clearance, dd. 

        Returns
        -------
            A Radiation object.
        """
        pass

    def setValues(self):
        """This method modifies the Radiation object.
        """
        pass
