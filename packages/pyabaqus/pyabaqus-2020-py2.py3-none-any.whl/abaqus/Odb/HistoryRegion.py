import typing

from abaqusConstants import *
from .HistoryOutput import HistoryOutput
from .HistoryPoint import HistoryPoint


class HistoryRegion:
    """The HistoryRegion object contains history data for a single location in the model.

    Attributes
    ----------
    position: SymbolicConstant
        A SymbolicConstant specifying the position of the history output. Possible values are
        NODAL, INTEGRATION_POINT, WHOLE_ELEMENT, WHOLE_REGION, and WHOLE_MODEL.
    historyOutputs: dict[str, HistoryOutput]
        A repository of :py:class:`~abaqus.Odb.HistoryOutput.HistoryOutput` objects.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import odbAccess
        session.odbs[name].steps[name].historyRegions[name]

    """

    # A SymbolicConstant specifying the position of the history output. Possible values are 
    # NODAL, INTEGRATION_POINT, WHOLE_ELEMENT, WHOLE_REGION, and WHOLE_MODEL. 
    position: SymbolicConstant = None

    # A repository of HistoryOutput objects. 
    historyOutputs: dict[str, HistoryOutput] = dict[str, HistoryOutput]()

    def __init__(self, name: str, description: str, point: HistoryPoint, loadCase: str = None):
        """This method creates a HistoryRegion object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            session.odbs[name].steps[name].HistoryRegion
        
        Parameters
        ----------
        name
            A String specifying the name of the HistoryRegion object. 
        description
            A String specifying the description of the HistoryRegion object. 
        point
            A HistoryPoint object specifying the point to which the history data refer. 
        loadCase
            None or an OdbLoadCase object specifying the load case associated with the HistoryRegion 
            object. The default value is None. 

        Returns
        -------
            A HistoryRegion object.
        """
        pass

    @typing.overload
    def getSubset(self, variableName: str):
        """This method returns a subset of the data in the HistoryRegion object.
        
        Parameters
        ----------
        variableName
            A String specifying the name of the output variable to return. 

        Returns
        -------
            A HistoryRegion object.
        """
        pass

    @typing.overload
    def getSubset(self, start: float):
        """This method returns a subset of the data in the HistoryRegion object.
        
        Parameters
        ----------
        start
            A Float specifying the start of the subset. This is the same as the first item in the 
            data array member of the HistoryOutput object. 

        Returns
        -------
            A HistoryRegion object.
        """
        pass

    @typing.overload
    def getSubset(self, start: float, end: float):
        """This method returns a subset of the data in the HistoryRegion object.
        
        Parameters
        ----------
        start
            A Float specifying the start of the subset. This is the same as the first item in the 
            data array member of the HistoryOutput object. 
        end
            A Float specifying the end of the subset. 

        Returns
        -------
            A HistoryRegion object.
        """
        pass

    def getSubset(self, *args, **kwargs):
        pass

    def HistoryOutput(self, name: str, description: str, type: SymbolicConstant,
                      validInvariants: SymbolicConstant = None):
        """This method creates a HistoryOutput object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            session.odbs[name].steps[name].HistoryRegion
        
        Parameters
        ----------
        name
            A String specifying the output variable name.
        description
            A String specifying the output variable.
        type
            A SymbolicConstant specifying the output type. Only SCALAR is currently supported.
        validInvariants
            A sequence of SymbolicConstants specifying which invariants should be calculated for
            this field. Possible values are MAGNITUDE, MISES, TRESCA, PRESS, INV3, MAX_PRINCIPAL,
            MID_PRINCIPAL, and MIN_PRINCIPAL. The default value is an empty sequence.

        Returns
        -------
            A HistoryOutput object.
        """
        self.historyOutputs[name] = historyOutput = HistoryOutput(name, description, type, validInvariants)
        return historyOutput
