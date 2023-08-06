from ..Calibration.Behavior import Behavior
from ..Calibration.DataSet import DataSet


class Calibration:
    """A Calibration object is the object used to specify a material calibration. The
    Calibration object stores the data that is used for specifying materials from test data. 

    Attributes
    ----------
    dataSets: DataSet
        A :py:class:`~abaqus.Calibration.DataSet.DataSet` object.
    behaviors: Behavior
        A :py:class:`~abaqus.Calibration.Behavior.Behavior` object.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import calibration
        mdb.models[name].calibrations[name]

    """

    # A DataSet object. 
    dataSets: DataSet = None

    # A Behavior object. 
    behaviors: Behavior = None

    def __init__(self, name: str):
        """This method creates a Calibration object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

                      mdb.models[name].Calibration
        
        Parameters
        ----------
        name
            A String specifying the name of the new calibration. 

        Returns
        -------
            A Calibration object.
        """
        pass
