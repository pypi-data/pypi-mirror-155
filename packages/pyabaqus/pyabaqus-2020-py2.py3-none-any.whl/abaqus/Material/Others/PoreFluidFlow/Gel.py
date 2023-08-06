class Gel:
    """The Gel object defines a swelling gel.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import material
        mdb.models[name].materials[name].gel
        import odbMaterial
        session.odbs[name].materials[name].gel

    The table data for this object are:

    - Radius of gel particles when completely dry, radry.
    - Fully swollen radius of gel particles, raf.
    - Number of gel particles per unit volume, ka.
    - Relaxation time constant for long-term swelling of gel particles, τ1.

    The corresponding analysis keywords are:

    - GEL

    """

    def __init__(self, table: tuple):
        """This method creates a Gel object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Gel
                session.odbs[name].materials[name].Gel
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 

        Returns
        -------
            A Gel object.
        """
        pass

    def setValues(self):
        """This method modifies the Gel object.
        """
        pass
