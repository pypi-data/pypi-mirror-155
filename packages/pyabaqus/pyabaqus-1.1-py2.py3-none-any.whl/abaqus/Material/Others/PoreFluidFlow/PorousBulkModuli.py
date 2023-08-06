from abaqusConstants import *


class PorousBulkModuli:
    """The PorousBulkModuli object defines bulk moduli for soils and rocks.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import material
        mdb.models[name].materials[name].porousBulkModuli
        import odbMaterial
        session.odbs[name].materials[name].porousBulkModuli

    The table data for this object are:

    - Bulk modulus of solid grains.
    - Bulk modulus of permeating fluid.
    - Temperature, if the data depend on temperature.

    The corresponding analysis keywords are:

    - POROUS BULK MODULI

    """

    def __init__(self, table: tuple, temperatureDependency: Boolean = OFF):
        """This method creates a PorousBulkModuli object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].PorousBulkModuli
                session.odbs[name].materials[name].PorousBulkModuli
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 

        Returns
        -------
            A PorousBulkModuli object.
        """
        pass

    def setValues(self):
        """This method modifies the PorousBulkModuli object.
        """
        pass
