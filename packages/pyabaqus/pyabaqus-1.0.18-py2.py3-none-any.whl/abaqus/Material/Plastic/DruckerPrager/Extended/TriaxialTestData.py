class TriaxialTestData:
    """The TriaxialTestData object provides triaxial test data.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import material
        mdb.models[name].materials[name].druckerPrager.triaxialTestData
        import odbMaterial
        session.odbs[name].materials[name].druckerPrager.triaxialTestData

    The table data for this object are:

    - Sign and magnitude of confining stress, σ1=σ2.
    - Sign and magnitude of the stress in loading direction, σ3.

    The corresponding analysis keywords are:

    - TRIAXIAL TEST DATA

    """

    def __init__(self, table: tuple, a: float = None, b: float = None, pt: float = None):
        """This method creates a TriaxialTestData object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].druckerPrager.TriaxialTestData
                session.odbs[name].materials[name].druckerPrager.TriaxialTestData
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        a
            None or a Float specifying the value of the material constant aa. None is used when the 
            value is unknown or it is not held fixed at the input value. The default value is None. 
        b
            None or a Float specifying the value of the material constant bb. None is used when the 
            value is unknown or it is not held fixed at the input value. The default value is None. 
        pt
            None or a Float specifying the value of the material constant pt. None is used when the 
            value is unknown or it is not held fixed at the input value. The default value is None. 

        Returns
        -------
            A TriaxialTestData object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the TriaxialTestData object.

        Raises
        ------
        RangeError
        """
        pass
