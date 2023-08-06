from abaqusConstants import *
from .AnalysisStep import AnalysisStep
from ..Adaptivity.AdaptiveMeshConstraintState import AdaptiveMeshConstraintState
from ..Adaptivity.AdaptiveMeshDomain import AdaptiveMeshDomain
from ..BoundaryCondition.BoundaryConditionState import BoundaryConditionState
from ..Load.LoadCase import LoadCase
from ..Load.LoadState import LoadState
from ..PredefinedField.PredefinedFieldState import PredefinedFieldState
from ..Region.Region import Region
from ..StepMiscellaneous.Control import Control
from ..StepMiscellaneous.SolverControl import SolverControl
from ..StepMiscellaneous.SubstructureGenerateFrequencyArray import SubstructureGenerateFrequencyArray
from ..StepMiscellaneous.SubstructureGenerateModesArray import SubstructureGenerateModesArray
from ..StepOutput.DiagnosticPrint import DiagnosticPrint
from ..StepOutput.FieldOutputRequestState import FieldOutputRequestState
from ..StepOutput.HistoryOutputRequestState import HistoryOutputRequestState
from ..StepOutput.Monitor import Monitor
from ..StepOutput.Restart import Restart


class SubstructureGenerateStep(AnalysisStep):
    """TheSubstructureGenerateStep object is used to generate a substructure.
    The SubstructureGenerateStep object is derived from the AnalysisStep object. 

    Attributes
    ----------
    name: str
        A String specifying the repository key.
    recoveryMatrix: SymbolicConstant
        A SymbolicConstant specifying the subtructure recovery to be computed. Possible values
        are WHOLE_MODEL, REGION, and NONE. The default value is WHOLE_MODEL.
    frequency: float
        A Float specifying the frequency at which to evaluate the frequency dependent
        properties. The default value is 0.0.
    retainedEigenmodesMethod: SymbolicConstant
        A SymbolicConstant specifying the eigenmodes to be retained. Possible values are
        MODE_RANGE, FREQUENCY_RANGE, and NONE. The default value is NONE.
    globalDampingField: SymbolicConstant
        A SymbolicConstant specifying the field to which the global damping factors should be
        applied. Possible values are ALL, ACOUSTIC, MECHANICAL, and NONE. The default value is
        NONE.
    alphaDampingRatio: float
        A Float specifying the factor to create global Rayleigh mass proportional damping. The
        default value is 0.0.
    betaDampingRatio: float
        A Float specifying the factor to create global Rayleigh stiffness proportional damping.
        The default value is 0.0.
    structuralDampingRatio: float
        A Float specifying the factor to create frequency-independent stiffness proportional
        structural damping. The default value is 0.0.
    viscousDampingControl: SymbolicConstant
        A SymbolicConstant specifying the damping control to include the viscous damping matrix.
        Possible values are ELEMENT, FACTOR, COMBINED, and NONE. The default value is NONE.
    structuralDampingControl: SymbolicConstant
        A SymbolicConstant specifying the damping control to include the structural damping
        matrix. Possible values are ELEMENT, FACTOR, COMBINED, and NONE. The default value is
        NONE.
    previous: str
        A String specifying the name of the previous step. The new step appears after this step
        in the list of analysis steps.
    description: str
        A String specifying a description of the new step. The default value is an empty string.
    substructureIdentifier: str
        A String specifying a unique identifier for the substructure. The default value is an
        empty string.
    recoveryRegion: Region
        A :py:class:`~abaqus.Region.Region.Region` object specifying the region for substructure recovery. This argument is
        required when **recoveryMatrix=REGION**.
    frequencyRange: SubstructureGenerateFrequencyArray
        A :py:class:`~abaqus.StepMiscellaneous.SubstructureGenerateFrequencyArray.SubstructureGenerateFrequencyArray` object.
    modeRange: SubstructureGenerateModesArray
        A :py:class:`~abaqus.StepMiscellaneous.SubstructureGenerateModesArray.SubstructureGenerateModesArray` object.
    explicit: SymbolicConstant
        A SymbolicConstant specifying whether the step has an explicit procedure type
        (**procedureType=ANNEAL**, DYNAMIC_EXPLICIT, or DYNAMIC_TEMP_DISPLACEMENT).
    perturbation: Boolean
        A Boolean specifying whether the step has a perturbation procedure type.
    nonmechanical: Boolean
        A Boolean specifying whether the step has a mechanical procedure type.
    procedureType: SymbolicConstant
        A SymbolicConstant specifying the Abaqus procedure. Possible values are:
            - ANNEAL
            - BUCKLE
            - COMPLEX_FREQUENCY
            - COUPLED_TEMP_DISPLACEMENT
            - COUPLED_THERMAL_ELECTRIC
            - DIRECT_CYCLIC
            - DYNAMIC_IMPLICIT
            - DYNAMIC_EXPLICIT
            - DYNAMIC_SUBSPACE
            - DYNAMIC_TEMP_DISPLACEMENT
            - COUPLED_THERMAL_ELECTRICAL_STRUCTURAL
            - FREQUENCY
            - GEOSTATIC
            - HEAT_TRANSFER
            - MASS_DIFFUSION
            - MODAL_DYNAMICS
            - RANDOM_RESPONSE
            - RESPONSE_SPECTRUM
            - SOILS
            - STATIC_GENERAL
            - STATIC_LINEAR_PERTURBATION
            - STATIC_RIKS
            - STEADY_STATE_DIRECT
            - STEADY_STATE_MODAL
            - STEADY_STATE_SUBSPACE
            - VISCO
    suppressed: Boolean
        A Boolean specifying whether the step is suppressed or not. The default value is OFF.
    fieldOutputRequestState: dict[str, FieldOutputRequestState]
        A repository of :py:class:`~abaqus.StepOutput.FieldOutputRequestState.FieldOutputRequestState` objects.
    historyOutputRequestState: dict[str, HistoryOutputRequestState]
        A repository of :py:class:`~abaqus.StepOutput.HistoryOutputRequestState.HistoryOutputRequestState` objects.
    diagnosticPrint: DiagnosticPrint
        A :py:class:`~abaqus.StepOutput.DiagnosticPrint.DiagnosticPrint` object.
    monitor: Monitor
        A :py:class:`~abaqus.StepOutput.Monitor.Monitor` object.
    restart: Restart
        A :py:class:`~abaqus.StepOutput.Restart.Restart` object.
    adaptiveMeshConstraintStates: dict[str, AdaptiveMeshConstraintState]
        A repository of :py:class:`~abaqus.Adaptivity.AdaptiveMeshConstraintState.AdaptiveMeshConstraintState` objects.
    adaptiveMeshDomains: dict[str, AdaptiveMeshDomain]
        A repository of :py:class:`~abaqus.Adaptivity.AdaptiveMeshDomain.AdaptiveMeshDomain` objects.
    control: Control
        A :py:class:`~abaqus.StepMiscellaneous.Control.Control` object.
    solverControl: SolverControl
        A :py:class:`~abaqus.StepMiscellaneous.SolverControl.SolverControl` object.
    boundaryConditionStates: dict[str, BoundaryConditionState]
        A repository of :py:class:`~abaqus.BoundaryCondition.BoundaryConditionState.BoundaryConditionState` objects.
    interactionStates: int
        A repository of :py:class:`~abaqus.Interaction.InteractionState.InteractionState` objects.
    loadStates: dict[str, LoadState]
        A repository of :py:class:`~abaqus.Load.LoadState.LoadState` objects.
    loadCases: dict[str, LoadCase]
        A repository of :py:class:`~abaqus.Load.LoadCase.LoadCase` objects.
    predefinedFieldStates: dict[str, PredefinedFieldState]
        A repository of :py:class:`~abaqus.PredefinedField.PredefinedFieldState.PredefinedFieldState` objects.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import step
        mdb.models[name].steps[name]

    The corresponding analysis keywords are:

    - SUBSTRUCTURE GENERATE
            - STEP

    """

    # A String specifying the repository key. 
    name: str = ''

    # A SymbolicConstant specifying the subtructure recovery to be computed. Possible values 
    # are WHOLE_MODEL, REGION, and NONE. The default value is WHOLE_MODEL. 
    recoveryMatrix: SymbolicConstant = WHOLE_MODEL

    # A Float specifying the frequency at which to evaluate the frequency dependent 
    # properties. The default value is 0.0. 
    frequency: float = 0

    # A SymbolicConstant specifying the eigenmodes to be retained. Possible values are 
    # MODE_RANGE, FREQUENCY_RANGE, and NONE. The default value is NONE. 
    retainedEigenmodesMethod: SymbolicConstant = NONE

    # A SymbolicConstant specifying the field to which the global damping factors should be 
    # applied. Possible values are ALL, ACOUSTIC, MECHANICAL, and NONE. The default value is 
    # NONE. 
    globalDampingField: SymbolicConstant = NONE

    # A Float specifying the factor to create global Rayleigh mass proportional damping. The 
    # default value is 0.0. 
    alphaDampingRatio: float = 0

    # A Float specifying the factor to create global Rayleigh stiffness proportional damping. 
    # The default value is 0.0. 
    betaDampingRatio: float = 0

    # A Float specifying the factor to create frequency-independent stiffness proportional 
    # structural damping. The default value is 0.0. 
    structuralDampingRatio: float = 0

    # A SymbolicConstant specifying the damping control to include the viscous damping matrix. 
    # Possible values are ELEMENT, FACTOR, COMBINED, and NONE. The default value is NONE. 
    viscousDampingControl: SymbolicConstant = NONE

    # A SymbolicConstant specifying the damping control to include the structural damping 
    # matrix. Possible values are ELEMENT, FACTOR, COMBINED, and NONE. The default value is 
    # NONE. 
    structuralDampingControl: SymbolicConstant = NONE

    # A String specifying the name of the previous step. The new step appears after this step 
    # in the list of analysis steps. 
    previous: str = ''

    # A String specifying a description of the new step. The default value is an empty string. 
    description: str = ''

    # A String specifying a unique identifier for the substructure. The default value is an 
    # empty string. 
    substructureIdentifier: str = ''

    # A Region object specifying the region for substructure recovery. This argument is 
    # required when *recoveryMatrix*=REGION. 
    recoveryRegion: Region = Region()

    # A SubstructureGenerateFrequencyArray object. 
    frequencyRange: SubstructureGenerateFrequencyArray = SubstructureGenerateFrequencyArray()

    # A SubstructureGenerateModesArray object. 
    modeRange: SubstructureGenerateModesArray = SubstructureGenerateModesArray()

    # A SymbolicConstant specifying whether the step has an explicit procedure type 
    # (*procedureType*=ANNEAL, DYNAMIC_EXPLICIT, or DYNAMIC_TEMP_DISPLACEMENT). 
    explicit: SymbolicConstant = None

    # A Boolean specifying whether the step has a perturbation procedure type. 
    perturbation: Boolean = OFF

    # A Boolean specifying whether the step has a mechanical procedure type. 
    nonmechanical: Boolean = OFF

    # A SymbolicConstant specifying the Abaqus procedure. Possible values are: 
    # - ANNEAL 
    # - BUCKLE 
    # - COMPLEX_FREQUENCY 
    # - COUPLED_TEMP_DISPLACEMENT 
    # - COUPLED_THERMAL_ELECTRIC 
    # - DIRECT_CYCLIC 
    # - DYNAMIC_IMPLICIT 
    # - DYNAMIC_EXPLICIT 
    # - DYNAMIC_SUBSPACE 
    # - DYNAMIC_TEMP_DISPLACEMENT 
    # - COUPLED_THERMAL_ELECTRICAL_STRUCTURAL 
    # - FREQUENCY 
    # - GEOSTATIC 
    # - HEAT_TRANSFER 
    # - MASS_DIFFUSION 
    # - MODAL_DYNAMICS 
    # - RANDOM_RESPONSE 
    # - RESPONSE_SPECTRUM 
    # - SOILS 
    # - STATIC_GENERAL 
    # - STATIC_LINEAR_PERTURBATION 
    # - STATIC_RIKS 
    # - STEADY_STATE_DIRECT 
    # - STEADY_STATE_MODAL 
    # - STEADY_STATE_SUBSPACE 
    # - VISCO 
    procedureType: SymbolicConstant = None

    # A Boolean specifying whether the step is suppressed or not. The default value is OFF. 
    suppressed: Boolean = OFF

    # A repository of FieldOutputRequestState objects. 
    fieldOutputRequestState: dict[str, FieldOutputRequestState] = dict[str, FieldOutputRequestState]()

    # A repository of HistoryOutputRequestState objects. 
    historyOutputRequestState: dict[str, HistoryOutputRequestState] = dict[str, HistoryOutputRequestState]()

    # A DiagnosticPrint object. 
    diagnosticPrint: DiagnosticPrint = DiagnosticPrint()

    # A Monitor object. 
    monitor: Monitor = None

    # A Restart object. 
    restart: Restart = Restart()

    # A repository of AdaptiveMeshConstraintState objects. 
    adaptiveMeshConstraintStates: dict[str, AdaptiveMeshConstraintState] = dict[
        str, AdaptiveMeshConstraintState]()

    # A repository of AdaptiveMeshDomain objects. 
    adaptiveMeshDomains: dict[str, AdaptiveMeshDomain] = dict[str, AdaptiveMeshDomain]()

    # A Control object. 
    control: Control = Control()

    # A SolverControl object. 
    solverControl: SolverControl = SolverControl()

    # A repository of BoundaryConditionState objects. 
    boundaryConditionStates: dict[str, BoundaryConditionState] = dict[str, BoundaryConditionState]()

    # A repository of InteractionState objects. 
    interactionStates: int = None

    # A repository of LoadState objects. 
    loadStates: dict[str, LoadState] = dict[str, LoadState]()

    # A repository of LoadCase objects. 
    loadCases: dict[str, LoadCase] = dict[str, LoadCase]()

    # A repository of PredefinedFieldState objects. 
    predefinedFieldStates: dict[str, PredefinedFieldState] = dict[str, PredefinedFieldState]()

    def __init__(self, name: str, previous: str, substructureIdentifier: int, description: str = '',
                 recoveryMatrix: SymbolicConstant = WHOLE_MODEL, recoveryRegion: Region = Region(),
                 computeGravityLoadVectors: Boolean = False, computeReducedMassMatrix: Boolean = False,
                 computeReducedStructuralDampingMatrix: Boolean = False,
                 computeReducedViscousDampingMatrix: Boolean = False,
                 evaluateFrequencyDependentProperties: Boolean = False, frequency: float = 0,
                 retainedEigenmodesMethod: SymbolicConstant = NONE,
                 modeRange: SubstructureGenerateModesArray = None,
                 frequencyRange: SubstructureGenerateFrequencyArray = None,
                 globalDampingField: SymbolicConstant = NONE, alphaDampingRatio: float = 0,
                 betaDampingRatio: float = 0, structuralDampingRatio: float = 0,
                 viscousDampingControl: SymbolicConstant = NONE,
                 structuralDampingControl: SymbolicConstant = NONE):
        """This method creates a SubstructureGenerateStep object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].SubstructureGenerateStep
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        previous
            A String specifying the name of the previous step. The new step appears after this step 
            in the list of analysis steps. 
        substructureIdentifier
            An Integer specifying a unique identifier for the substructure. 
        description
            A String specifying a description of the new step. The default value is an empty string. 
        recoveryMatrix
            A SymbolicConstant specifying the subtructure recovery to be computed. Possible values 
            are WHOLE_MODEL, REGION, and NONE. The default value is WHOLE_MODEL. 
        recoveryRegion
            A Region object specifying the region for substructure recovery. This argument is 
            required when *recoveryMatrix*=REGION. 
        computeGravityLoadVectors
            A Boolean specifying whether to compute the gravity load vectors. The default value is 
            False. 
        computeReducedMassMatrix
            A Boolean specifying whether to compute the reduced mass matrix. The default value is 
            False. 
        computeReducedStructuralDampingMatrix
            A Boolean specifying whether to compute the reduced structural damping matrix. The 
            default value is False. 
        computeReducedViscousDampingMatrix
            A Boolean specifying whether to compute the reduced viscous damping matrix. The default 
            value is False. 
        evaluateFrequencyDependentProperties
            A Boolean specifying whether to evaluate the frequency dependent properties. The default 
            value is False. 
        frequency
            A Float specifying the frequency at which to evaluate the frequency dependent 
            properties. The default value is 0.0. 
        retainedEigenmodesMethod
            A SymbolicConstant specifying the eigenmodes to be retained. Possible values are 
            MODE_RANGE, FREQUENCY_RANGE, and NONE. The default value is NONE. 
        modeRange
            A SubstructureGenerateModesArray object. 
        frequencyRange
            A SubstructureGenerateFrequencyArray object. 
        globalDampingField
            A SymbolicConstant specifying the field to which the global damping factors should be 
            applied. Possible values are ALL, ACOUSTIC, MECHANICAL, and NONE. The default value is 
            NONE. 
        alphaDampingRatio
            A Float specifying the factor to create global Rayleigh mass proportional damping. The 
            default value is 0.0. 
        betaDampingRatio
            A Float specifying the factor to create global Rayleigh stiffness proportional damping. 
            The default value is 0.0. 
        structuralDampingRatio
            A Float specifying the factor to create frequency-independent stiffness proportional 
            structural damping. The default value is 0.0. 
        viscousDampingControl
            A SymbolicConstant specifying the damping control to include the viscous damping matrix. 
            Possible values are ELEMENT, FACTOR, COMBINED, and NONE. The default value is NONE. 
        structuralDampingControl
            A SymbolicConstant specifying the damping control to include the structural damping 
            matrix. Possible values are ELEMENT, FACTOR, COMBINED, and NONE. The default value is 
            NONE. 

        Returns
        -------
            A SubstructureGenerateStep object. 

        Raises
        ------
        RangeError
        """
        super().__init__()
        pass

    def setValues(self, description: str = '', recoveryMatrix: SymbolicConstant = WHOLE_MODEL,
                  recoveryRegion: Region = Region(), computeGravityLoadVectors: Boolean = False,
                  computeReducedMassMatrix: Boolean = False,
                  computeReducedStructuralDampingMatrix: Boolean = False,
                  computeReducedViscousDampingMatrix: Boolean = False,
                  evaluateFrequencyDependentProperties: Boolean = False, frequency: float = 0,
                  retainedEigenmodesMethod: SymbolicConstant = NONE,
                  modeRange: SubstructureGenerateModesArray = None,
                  frequencyRange: SubstructureGenerateFrequencyArray = None,
                  globalDampingField: SymbolicConstant = NONE, alphaDampingRatio: float = 0,
                  betaDampingRatio: float = 0, structuralDampingRatio: float = 0,
                  viscousDampingControl: SymbolicConstant = NONE,
                  structuralDampingControl: SymbolicConstant = NONE):
        """This method modifies the SubstructureGenerateStep object.
        
        Parameters
        ----------
        description
            A String specifying a description of the new step. The default value is an empty string. 
        recoveryMatrix
            A SymbolicConstant specifying the subtructure recovery to be computed. Possible values 
            are WHOLE_MODEL, REGION, and NONE. The default value is WHOLE_MODEL. 
        recoveryRegion
            A Region object specifying the region for substructure recovery. This argument is 
            required when *recoveryMatrix*=REGION. 
        computeGravityLoadVectors
            A Boolean specifying whether to compute the gravity load vectors. The default value is 
            False. 
        computeReducedMassMatrix
            A Boolean specifying whether to compute the reduced mass matrix. The default value is 
            False. 
        computeReducedStructuralDampingMatrix
            A Boolean specifying whether to compute the reduced structural damping matrix. The 
            default value is False. 
        computeReducedViscousDampingMatrix
            A Boolean specifying whether to compute the reduced viscous damping matrix. The default 
            value is False. 
        evaluateFrequencyDependentProperties
            A Boolean specifying whether to evaluate the frequency dependent properties. The default 
            value is False. 
        frequency
            A Float specifying the frequency at which to evaluate the frequency dependent 
            properties. The default value is 0.0. 
        retainedEigenmodesMethod
            A SymbolicConstant specifying the eigenmodes to be retained. Possible values are 
            MODE_RANGE, FREQUENCY_RANGE, and NONE. The default value is NONE. 
        modeRange
            A SubstructureGenerateModesArray object. 
        frequencyRange
            A SubstructureGenerateFrequencyArray object. 
        globalDampingField
            A SymbolicConstant specifying the field to which the global damping factors should be 
            applied. Possible values are ALL, ACOUSTIC, MECHANICAL, and NONE. The default value is 
            NONE. 
        alphaDampingRatio
            A Float specifying the factor to create global Rayleigh mass proportional damping. The 
            default value is 0.0. 
        betaDampingRatio
            A Float specifying the factor to create global Rayleigh stiffness proportional damping. 
            The default value is 0.0. 
        structuralDampingRatio
            A Float specifying the factor to create frequency-independent stiffness proportional 
            structural damping. The default value is 0.0. 
        viscousDampingControl
            A SymbolicConstant specifying the damping control to include the viscous damping matrix. 
            Possible values are ELEMENT, FACTOR, COMBINED, and NONE. The default value is NONE. 
        structuralDampingControl
            A SymbolicConstant specifying the damping control to include the structural damping 
            matrix. Possible values are ELEMENT, FACTOR, COMBINED, and NONE. The default value is 
            NONE.

        Raises
        ------
        RangeError
        """
        pass
