from .Section import Section


class AcousticInterfaceSection(Section):
    """The AcousticInterfaceSection object defines the properties of an acoustic section.
    The AcousticInterfaceSection object is derived from the Section object. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import section
        mdb.models[name].sections[name]
        import odbSection
        session.odbs[name].sections[name]

    The corresponding analysis keywords are:

    - INTERFACE

    """

    def __init__(self, name: str, thickness: float = 1):
        """This method creates an AcousticInterfaceSection object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].AcousticInterfaceSection
            session.odbs[name].AcousticInterfaceSection
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        thickness
            A Float specifying the thickness of the section. Possible values are *thickness* >> 0.0. 
            The default value is 1.0. 

        Returns
        -------
            An AcousticInterfaceSection object. 
            
        Raises
        ------
        InvalidNameError
        RangeError 
        """
        super().__init__()
        pass

    def setValues(self, thickness: float = 1):
        """This method modifies the AcousticInterfaceSection object.
        
        Parameters
        ----------
        thickness
            A Float specifying the thickness of the section. Possible values are *thickness* >> 0.0. 
            The default value is 1.0.

        Raises
        ------
        RangeError
        """
        pass
