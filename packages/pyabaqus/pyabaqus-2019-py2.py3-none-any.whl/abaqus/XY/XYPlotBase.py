from abaqusConstants import *
from .Area import Area
from .Chart import Chart
from .Title import Title
from .XYCurve import XYCurve


class XYPlotBase:
    """The XYPlot object is used to display Chart objects.

    Attributes
    ----------
    area: Area
        An :py:class:`~abaqus.XY.Area.Area` object specifying position, padding, background and borders of the XYPlot
        object.
    title: Title
        A :py:class:`~abaqus.XY.Title.Title` object specifying the title of the :py:class:`~abaqus.XY.XYPlot.XYPlot` object.
    charts: dict[str, Chart]
        A repository of :py:class:`~abaqus.XY.Chart.Chart` objects.
    curves: dict[str, XYCurve]
        A repository of :py:class:`~abaqus.XY.XYCurve.XYCurve` objects.
    transform: float
        A tuple of Floats specifying a transformation matrix used to scale or pan along the axes
        of the active :py:class:`~abaqus.XY.Chart.Chart` object of this XYPlot.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import visualization
        session.xyPlots[name]

    """

    # An Area object specifying position, padding, background and borders of the XYPlot 
    # object. 
    area: Area = Area()

    # A Title object specifying the title of the XYPlot object. 
    title: Title = Title()

    # A repository of Chart objects. 
    charts: dict[str, Chart] = dict[str, Chart]()

    # A repository of XYCurve objects. 
    curves: dict[str, XYCurve] = dict[str, XYCurve]()

    # A tuple of Floats specifying a transformation matrix used to scale or pan along the axes 
    # of the active Chart object of this XYPlot. 
    transform: float = None

    def __init__(self, name: str):
        """This method creates an empty XYPlot object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            session.XYPlot
        
        Parameters
        ----------
        name
            A String specifying the name of the XYPlot object. 

        Returns
        -------
            An XYPlot object.
        """
        pass

    def autoColor(self, lines: Boolean = OFF, symbols: Boolean = OFF):
        """This method distributes the colors on all curves displayed in the XYPlot using the color
        palette defined by the xyColors AutoColors object.
        
        Parameters
        ----------
        lines
            A Boolean defining whether color distribution affects curve lines. 
        symbols
            A Boolean defining whether color distribution affects curve symbols. 
        """
        pass

    def autoSymbol(self):
        """This method distributes the symbols on all curves displayed in the XYPlot.
        """
        pass

    def fitCurves(self):
        """This method resets the transform of all the charts of the XYPlot object. It cancels any
        zoom or pan action.
        """
        pass

    def next(self, drawImmediately: Boolean = False):
        """This method restores the *transform* member of the active Chart object to the next
        setting in the transform list. (There is a list of eight transforms stored for each
        chart.) If there is no next transform, no action is taken.
        
        Parameters
        ----------
        drawImmediately
            A Boolean specifying the viewport should refresh immediately after the command is 
            processed. This is typically only used when writing a script and it is desirable to show 
            intermediate results before the script completes. The default value is False. 
        """
        pass

    def previous(self, drawImmediately: Boolean = False):
        """This method restores the *transform* member of the active Chart object to the previous
        setting in the transform list. (There is a list of eight transforms stored for each
        chart.) If there is no next transform, no action is taken.
        
        Parameters
        ----------
        drawImmediately
            A Boolean specifying the viewport should refresh immediately after the command is 
            processed. This is typically only used when writing a script and it is desirable to show 
            intermediate results before the script completes. The default value is False. 
        """
        pass

    def setValues(self, title: Title = Title(), transform: tuple = ()):
        """This method modifies the XYPlot object.
        
        Parameters
        ----------
        title
            A Title object specifying the title of the XYPlot object. 
        transform
            A sequence of Floats specifying a transformation matrix used to scale or pan along the 
            axes of the active Chart object of this XYPlot. 
        """
        pass
