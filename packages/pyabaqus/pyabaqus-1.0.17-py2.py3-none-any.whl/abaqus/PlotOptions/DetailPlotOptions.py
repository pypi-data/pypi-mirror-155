from .PlyStackPlotOptions import PlyStackPlotOptions


class DetailPlotOptions:
    """The DetailPlotOptions object stores values and attributes associated with a Viewport
    object. The DetailPlotOptions object has no constructor command. Abaqus creates the 
    *detailPlotOptions* member whenever a Viewport is created. 

    Attributes
    ----------
    plyStackPlotOptions: PlyStackPlotOptions
        A :py:class:`~abaqus.PlotOptions.PlyStackPlotOptions.PlyStackPlotOptions` object.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python
    
        session.viewports[name].detailPlotOptions

    """

    # A PlyStackPlotOptions object. 
    plyStackPlotOptions: PlyStackPlotOptions = PlyStackPlotOptions()
