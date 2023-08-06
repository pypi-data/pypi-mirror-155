from .RayleighDampingByFrequencyComponentArray import RayleighDampingByFrequencyComponentArray


class RayleighDampingByFrequency:
    """A RayleighDampingByFrequency object contains Rayleigh Damping parameters.

    Attributes
    ----------
    components: RayleighDampingByFrequencyComponentArray
        A :py:class:`~abaqus.StepMiscellaneous.RayleighDampingByFrequencyComponentArray.RayleighDampingByFrequencyComponentArray` object.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
    
        import step
        mdb.models[name].steps[name].rayleighDampingByFrequency

    """

    # A RayleighDampingByFrequencyComponentArray object. 
    components: RayleighDampingByFrequencyComponentArray = RayleighDampingByFrequencyComponentArray()
