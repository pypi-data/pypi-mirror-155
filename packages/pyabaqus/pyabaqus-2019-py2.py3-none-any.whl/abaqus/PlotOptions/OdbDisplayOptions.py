from .DGCommonOptions import DGCommonOptions
from .DGContourOptions import DGContourOptions
from .DGDisplayBodyOptions import DGDisplayBodyOptions
from .DGOrientationOptions import DGOrientationOptions
from .DGSuperimposeOptions import DGSuperimposeOptions
from .DGSymbolOptions import DGSymbolOptions


class OdbDisplayOptions:
    """The OdbDisplayOptions object stores the display options associated with an OdbInstance
    object. This object does not have a constructor. Abaqus creates the OdbDisplayOptions 
    object when an OdbInstance object is created using the display options associated with 
    the current viewport at the time of creation. 

    Attributes
    ----------
    commonOptions: DGCommonOptions
        A :py:class:`~abaqus.PlotOptions.DGCommonOptions.DGCommonOptions` object.
    superimposeOptions: DGSuperimposeOptions
        A :py:class:`~abaqus.PlotOptions.DGSuperimposeOptions.DGSuperimposeOptions` object.
    contourOptions: DGContourOptions
        A :py:class:`~abaqus.PlotOptions.DGContourOptions.DGContourOptions` object.
    symbolOptions: DGSymbolOptions
        A :py:class:`~abaqus.PlotOptions.DGSymbolOptions.DGSymbolOptions` object.
    materialOrientationOptions: DGOrientationOptions
        A :py:class:`~abaqus.PlotOptions.DGOrientationOptions.DGOrientationOptions` object.
    displayBodyOptions: DGDisplayBodyOptions
        A :py:class:`~abaqus.PlotOptions.DGDisplayBodyOptions.DGDisplayBodyOptions` object.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import assembly
        session.viewports[name].assemblyDisplay.displayGroupInstances[name].odbDisplayOptions
        session.viewports[name].layers[name].assemblyDisplay.displayGroupInstances[name].odbDisplayOptions
        import visualization
        session.viewports[name].layers[name].odbDisplay.displayGroupInstances[name].odbDisplayOptions
        import part
        session.viewports[name].layers[name].partDisplay.displayGroupInstances[name].odbDisplayOptions
        session.viewports[name].odbDisplay.displayGroupInstances[name].odbDisplayOptions
        session.viewports[name].partDisplay.displayGroupInstances[name].odbDisplayOptions

    """

    # A DGCommonOptions object. 
    commonOptions: DGCommonOptions = DGCommonOptions()

    # A DGSuperimposeOptions object. 
    superimposeOptions: DGSuperimposeOptions = DGSuperimposeOptions()

    # A DGContourOptions object. 
    contourOptions: DGContourOptions = DGContourOptions()

    # A DGSymbolOptions object. 
    symbolOptions: DGSymbolOptions = DGSymbolOptions()

    # A DGOrientationOptions object. 
    materialOrientationOptions: DGOrientationOptions = DGOrientationOptions()

    # A DGDisplayBodyOptions object. 
    displayBodyOptions: DGDisplayBodyOptions = DGDisplayBodyOptions()
