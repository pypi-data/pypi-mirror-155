from abaqusConstants import *
from .AreaStyle import AreaStyle
from .LineStyle import LineStyle


class Area:
    """The Area object is used to display a rectangular area in an XYPlot. The Area object has
    no constructor. Area objects are automatically created whenever a XYPlot, Chart, 
    PlotTitle, or Legend objects are created. 

    Attributes
    ----------
    inset: Boolean
        A Boolean specifying whether the area is inset or occupies a reserved area. The default
        value is OFF.
    positionMethod: SymbolicConstant
        A SymbolicConstant specifying how the area is positioned. Possible values are AUTO_ALIGN
        and MANUAL. The default value is AUTO_ALIGN.
    alignment: SymbolicConstant
        A SymbolicConstant specifying the relative position of the area in its parent when
        **positionMethod=AUTO_ALIGN**. Possible values are:
            - BOTTOM_LEFT
            - BOTTOM_CENTER
            - BOTTOM_RIGHT
            - CENTER_LEFT
            - CENTER
            - CENTER_RIGHT
            - TOP_LEFT
            - TOP_CENTER
            - TOP_RIGHT
        The default value is BOTTOM_LEFT.
    sizeMethod: SymbolicConstant
        A SymbolicConstant specifying how the area size is defined. Possible values are
        AUTOMATIC and MANUAL. The default value is AUTOMATIC.
    width: float
        A Float specifying the width of the area in mm. The default value is 1.0.
    height: float
        A Float specifying the height of the area in mm. The default value is 1.0.
    widthScale: float
        A Float specifying the scale as a fraction of the width of the available area when the
        sizeMethod=MANUAL. The valid range is (0, 1). The default value is 1.0.
    heightScale: float
        A Float specifying the scale as a fraction of the height of the available area when the
        **sizeMethod=MANUAL**. The valid range is (0, 1). The default value is 1.0.
    pl: float
        A Float specifying the left padding of the area in mm. The default value is 1.0.
    pr: float
        A Float specifying the right padding of the area in mm. The default value is 1.0.
    pt: float
        A Float specifying the top padding of the area in mm. The default value is 1.0.
    pb: float
        A Float specifying the bottom padding of the area in mm. The default value is 1.0.
    style: AreaStyle
        An :py:class:`~abaqus.XY.AreaStyle.AreaStyle` object specifying whether and how to fill the area.
    border: LineStyle
        A :py:class:`~abaqus.XY.LineStyle.LineStyle` object specifying whether and how to draw the border of the area.
    origin: tuple[float]
        A pair of Floats specifying the X- and Y-offsets in millimeters from the lower-left
        corner of the XYPlot.
    originOffset: tuple[float]
        A pair of Floats specifying the X- and Y-offsets of the origin as a fraction of the
        available area. The **originOffset** argument is ignored unless **positionMethod=MANUAL**.
        The default value is (-1, 0). The valid range for each float is (0, 1).

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import visualization
        session.charts[name].area
        session.charts[name].gridArea
        session.charts[name].legend.area
        session.defaultChartOptions.gridArea
        session.defaultChartOptions.legend.area
        session.defaultPlot.area
        session.defaultPlot.title.area
        session.xyPlots[name].area
        session.xyPlots[name].charts[name].area
        session.xyPlots[name].charts[name].gridArea
        session.xyPlots[name].charts[name].legend.area
        session.xyPlots[name].title.area

    """

    # A Boolean specifying whether the area is inset or occupies a reserved area. The default 
    # value is OFF. 
    inset: Boolean = OFF

    # A SymbolicConstant specifying how the area is positioned. Possible values are AUTO_ALIGN 
    # and MANUAL. The default value is AUTO_ALIGN. 
    positionMethod: SymbolicConstant = AUTO_ALIGN

    # A SymbolicConstant specifying the relative position of the area in its parent when 
    # *positionMethod*=AUTO_ALIGN. Possible values are: 
    # - BOTTOM_LEFT 
    # - BOTTOM_CENTER 
    # - BOTTOM_RIGHT 
    # - CENTER_LEFT 
    # - CENTER 
    # - CENTER_RIGHT 
    # - TOP_LEFT 
    # - TOP_CENTER 
    # - TOP_RIGHT 
    # The default value is BOTTOM_LEFT. 
    alignment: SymbolicConstant = BOTTOM_LEFT

    # A SymbolicConstant specifying how the area size is defined. Possible values are 
    # AUTOMATIC and MANUAL. The default value is AUTOMATIC. 
    sizeMethod: SymbolicConstant = AUTOMATIC

    # A Float specifying the width of the area in mm. The default value is 1.0. 
    width: float = 1

    # A Float specifying the height of the area in mm. The default value is 1.0. 
    height: float = 1

    # A Float specifying the scale as a fraction of the width of the available area when the 
    # sizeMethod=MANUAL. The valid range is (0, 1). The default value is 1.0. 
    widthScale: float = 1

    # A Float specifying the scale as a fraction of the height of the available area when the 
    # *sizeMethod*=MANUAL. The valid range is (0, 1). The default value is 1.0. 
    heightScale: float = 1

    # A Float specifying the left padding of the area in mm. The default value is 1.0. 
    pl: float = 1

    # A Float specifying the right padding of the area in mm. The default value is 1.0. 
    pr: float = 1

    # A Float specifying the top padding of the area in mm. The default value is 1.0. 
    pt: float = 1

    # A Float specifying the bottom padding of the area in mm. The default value is 1.0. 
    pb: float = 1

    # An AreaStyle object specifying whether and how to fill the area. 
    style: AreaStyle = AreaStyle()

    # A LineStyle object specifying whether and how to draw the border of the area. 
    border: LineStyle = LineStyle()

    # A pair of Floats specifying the X- and Y-offsets in millimeters from the lower-left 
    # corner of the XYPlot. 
    origin: tuple[float] = ()

    # A pair of Floats specifying the X- and Y-offsets of the origin as a fraction of the 
    # available area. The *originOffset* argument is ignored unless *positionMethod*=MANUAL. 
    # The default value is (-1, 0). The valid range for each float is (0, 1). 
    originOffset: tuple[float] = ()

    def setValues(self, area: 'Area' = None, style: AreaStyle = AreaStyle(), border: LineStyle = LineStyle(),
                  positionMethod: SymbolicConstant = AUTO_ALIGN,
                  alignment: SymbolicConstant = BOTTOM_LEFT, sizeMethod: SymbolicConstant = AUTOMATIC,
                  originOffset: tuple[float] = (), widthScale: float = 1, heightScale: float = 1,
                  inset: Boolean = OFF, pl: float = 1, pr: float = 1, pt: float = 1, pb: float = 1):
        """This method modifies the Area object.
        
        Parameters
        ----------
        area
            An Area object from which attributes are to be copied. 
        style
            An AreaStyle object. 
        border
            A LineStyle object. 
        positionMethod
            A SymbolicConstant specifying how the area is positioned. Possible values are AUTO_ALIGN 
            and MANUAL. The default value is AUTO_ALIGN. 
        alignment
            A SymbolicConstant specifying the relative position of the area in its parent when 
            *positionMethod*=AUTO_ALIGN. Possible values are: 
            
            - BOTTOM_LEFT 
            - BOTTOM_CENTER 
            - BOTTOM_RIGHT 
            - CENTER_LEFT 
            - CENTER 
            - CENTER_RIGHT 
            - TOP_LEFT 
            - TOP_CENTER 
            - TOP_RIGHT 
            The default value is BOTTOM_LEFT. 
        sizeMethod
            A SymbolicConstant specifying how the area size is defined. Possible values are 
            AUTOMATIC and MANUAL. The default value is AUTOMATIC. 
        originOffset
            A pair of Floats specifying the X- and Y-offsets of the origin as a fraction of the 
            available area. The *originOffset* argument is ignored unless *positionMethod*=MANUAL. 
            The default value is (-1, 0). The valid range for each float is (0, 1). 
        widthScale
            A Float specifying the scale as a fraction of the width of the available area when the 
            sizeMethod=MANUAL. The valid range is (0, 1). The default value is 1.0. 
        heightScale
            A Float specifying the scale as a fraction of the height of the available area when the 
            *sizeMethod*=MANUAL. The valid range is (0, 1). The default value is 1.0. 
        inset
            A Boolean specifying whether the area is inset or occupies a reserved area. The default 
            value is OFF. 
        pl
            A Float specifying the left padding of the area in mm. The default value is 1.0. 
        pr
            A Float specifying the right padding of the area in mm. The default value is 1.0. 
        pt
            A Float specifying the top padding of the area in mm. The default value is 1.0. 
        pb
            A Float specifying the bottom padding of the area in mm. The default value is 1.0.

        Raises
        ------
        RangeError
        """
        pass
