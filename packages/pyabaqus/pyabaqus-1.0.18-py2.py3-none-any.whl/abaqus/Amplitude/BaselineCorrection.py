class BaselineCorrection:
    """The BaselineCorrection object modifies an acceleration history to minimize the overall
    drift of the displacement obtained from the time integration of the given acceleration. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import amplitude
        mdb.models[name].amplitudes[name].baselineCorrection
        import odbAmplitude
        session.odbs[name].amplitudes[name].baselineCorrection

    The corresponding analysis keywords are:

    - BASELINE CORRECTION

    """

    def __init__(self, intervals: tuple = ()):
        """This method creates a BaselineCorrection object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].amplitudes[name].BaselineCorrection
            session.odbs[name].amplitudes[name].BaselineCorrection
        
        Parameters
        ----------
        intervals
            A sequence of Floats specifying the correction time interval end points. Possible values 
            are positive and monotonically increasing Floats. The default value is an empty 
            sequence. 

        Returns
        -------
            A BaselineCorrection object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the BaselineCorrection object.

        Raises
        ------
        RangeError
        """
        pass
