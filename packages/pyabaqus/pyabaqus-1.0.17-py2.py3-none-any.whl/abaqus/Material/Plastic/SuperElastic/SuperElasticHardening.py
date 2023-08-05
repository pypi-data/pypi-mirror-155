class SuperElasticHardening:
    """The SuperElasticHardening object specifies the dependence of the yield stress on the
    total strain to define the piecewise linear hardening of a martensite material model. 

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import material
        mdb.models[name].materials[name].superElasticity.SuperElasticHardening
        import odbMaterial
        session.odbs[name].materials[name].superElasticity.SuperElasticHardening

    The table data for this object are:
    
    - Yield Stress.
    - Total Strain.

    The corresponding analysis keywords are:

    - SUPERELASTIC HARDENING

    """

    def __init__(self, table: tuple):
        """This method creates a SuperElasticHardening object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].superElasticity.SuperElasticHardening
                session.odbs[name].materials[name].superElasticity.SuperElasticHardening
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 

        Returns
        -------
            A SuperElasticHardening object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the SuperElasticHardening object.

        Raises
        ------
        RangeError
        """
        pass
