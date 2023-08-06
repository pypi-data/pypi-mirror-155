class OdbDataInstance:
    """The OdbDataInstance object instance data.

    Attributes
    ----------
    name: str
        A String specifying the instance name. This attribute is read-only.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import visualization
        session.odbData[name].instances[i]

    """

    # A String specifying the instance name. This attribute is read-only. 
    name: str = ''
