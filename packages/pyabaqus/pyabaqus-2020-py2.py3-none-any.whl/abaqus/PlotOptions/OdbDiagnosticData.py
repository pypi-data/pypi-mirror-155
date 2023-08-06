from abaqusConstants import *
from .OdbAnalysisError import OdbAnalysisError
from .OdbAnalysisWarning import OdbAnalysisWarning
from .OdbDiagnosticStep import OdbDiagnosticStep
from .OdbJobTime import OdbJobTime
from .OdbNumericalProblemSummary import OdbNumericalProblemSummary


class OdbDiagnosticData:
    """The OdbDiagnosticData object.

    Attributes
    ----------
    analysisErrors: dict[str, OdbAnalysisError]
        A repository of :py:class:`~abaqus.PlotOptions.OdbAnalysisError.OdbAnalysisError` objects.
    analysisWarnings: dict[str, OdbAnalysisWarning]
        A repository of :py:class:`~abaqus.PlotOptions.OdbAnalysisWarning.OdbAnalysisWarning` objects.
    steps: dict[str, OdbDiagnosticStep]
        A repository of :py:class:`~abaqus.PlotOptions.OdbDiagnosticStep.OdbDiagnosticStep` objects.
    jobTime: OdbJobTime
        An :py:class:`~abaqus.PlotOptions.OdbJobTime.OdbJobTime` object.
    numericalProblemSummary: OdbNumericalProblemSummary
        An :py:class:`~abaqus.PlotOptions.OdbNumericalProblemSummary.OdbNumericalProblemSummary` object.
    isXplDoublePrecision: Boolean
        A boolean specifying whether or not double precision is used for the analysis. This
        attribute is read-only.
    jobStatus: str
        A String specifying the job status after the analysis. This attribute is read-only.
    numDomains: str
        An int specifying the number of domains. This attribute is read-only.
    numberOfAnalysisErrors: str
        An int specifying the number of analysis errors encountered. This attribute is
        read-only.
    numberOfAnalysisWarnings: str
        An int specifying the number of analysis warnings encountered. This attribute is
        read-only.
    numberOfSteps: str
        An int specifying the number of steps present in the analysis. This attribute is
        read-only.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import visualization
        session.odbData[name].diagnosticData

    """

    # A repository of OdbAnalysisError objects. 
    analysisErrors: dict[str, OdbAnalysisError] = dict[str, OdbAnalysisError]()

    # A repository of OdbAnalysisWarning objects. 
    analysisWarnings: dict[str, OdbAnalysisWarning] = dict[str, OdbAnalysisWarning]()

    # A repository of OdbDiagnosticStep objects. 
    steps: dict[str, OdbDiagnosticStep] = dict[str, OdbDiagnosticStep]()

    # An OdbJobTime object. 
    jobTime: OdbJobTime = OdbJobTime()

    # An OdbNumericalProblemSummary object. 
    numericalProblemSummary: OdbNumericalProblemSummary = OdbNumericalProblemSummary()

    # A boolean specifying whether or not double precision is used for the analysis. This 
    # attribute is read-only. 
    isXplDoublePrecision: Boolean = OFF

    # A String specifying the job status after the analysis. This attribute is read-only. 
    jobStatus: str = ''

    # An int specifying the number of domains. This attribute is read-only. 
    numDomains: str = ''

    # An int specifying the number of analysis errors encountered. This attribute is 
    # read-only. 
    numberOfAnalysisErrors: str = ''

    # An int specifying the number of analysis warnings encountered. This attribute is 
    # read-only. 
    numberOfAnalysisWarnings: str = ''

    # An int specifying the number of steps present in the analysis. This attribute is 
    # read-only. 
    numberOfSteps: str = ''
