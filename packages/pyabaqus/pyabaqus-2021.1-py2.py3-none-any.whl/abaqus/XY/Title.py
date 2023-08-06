from abaqusConstants import *
from .Area import Area
from .TextStyle import TextStyle


class Title:
    """The Title object is used to store the display attributes of the XYPlot title. An Title
    object is automatically created when creating a XYPlot object. 

    Attributes
    ----------
    useDefault: Boolean
        A Boolean specifying whether to show the default title. The default value is OFF.
    area: Area
        An :py:class:`~abaqus.XY.Area.Area` object specifying the area of the title.
    text: str
        A String specifying the text to appear as a title. By default the title is set to the
        :py:class:`~abaqus.XY.XYPlot.XYPlot` object name. The default value is an empty string.
    titleStyle: TextStyle
        A :py:class:`~abaqus.XY.TextStyle.TextStyle` object specifying the text properties used to display the legend title.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import visualization
        session.defaultPlot.title
        session.xyPlots[name].title

    """

    # A Boolean specifying whether to show the default title. The default value is OFF. 
    useDefault: Boolean = OFF

    # An Area object specifying the area of the title. 
    area: Area = Area()

    # A String specifying the text to appear as a title. By default the title is set to the 
    # XYPlot object name. The default value is an empty string. 
    text: str = ''

    # A TextStyle object specifying the text properties used to display the legend title. 
    titleStyle: TextStyle = TextStyle()

    def setValues(self, title: 'Title' = None, text: str = '', area: Area = Area(),
                  useDefault: Boolean = OFF, titleStyle: TextStyle = TextStyle()):
        """This method modifies the Title object.
        
        Parameters
        ----------
        title
            A Title object from which attributes are to be copied. 
        text
            A String specifying the text to appear as a title. By default the title is set to the 
            XYPlot object name. The default value is an empty string. 
        area
            An Area object specifying the area of the title. 
        useDefault
            A Boolean specifying whether to show the default title. The default value is OFF. 
        titleStyle
            A TextStyle object specifying the text properties used to display the legend title. 
        """
        pass
