from abaqusConstants import *
from .OdbPart import OdbPart
from .OdbStep import OdbStep
from .SectionCategory import SectionCategory
from ..Amplitude.AmplitudeOdb import AmplitudeOdb
from ..BeamSectionProfile.BeamSectionProfileOdb import BeamSectionProfileOdb
from ..Filter.FilterOdb import FilterOdb
from ..Material.MaterialOdb import MaterialOdb


class Odb(AmplitudeOdb,
          FilterOdb,
          MaterialOdb,
          BeamSectionProfileOdb):
    """The Odb object is the in-memory representation of an output database (ODB) file.

    Attributes
    ----------
    isReadOnly: Boolean
        A Boolean specifying whether the output database was opened with read-only access.
    amplitudes: dict[str, Amplitude]
        A repository of :py:class:`~abaqus.Amplitude.Amplitude.Amplitude` objects.
    filters: dict[str, Filter]
        A repository of :py:class:`~abaqus.Filter.Filter.Filter` objects.
    rootAssembly: OdbAssembly
        An :py:class:`~abaqus.Odb.OdbAssembly.OdbAssembly` object.
    jobData: JobData
        A :py:class:`~abaqus.Odb.JobData.JobData` object.
    parts: dict[str, OdbPart]
        A repository of :py:class:`~abaqus.Odb.OdbPart.OdbPart` objects.
    materials: dict[str, Material]
        A repository of :py:class:`~abaqus.Material.Material.Material` objects.
    steps: dict[str, OdbStep]
        A repository of :py:class:`~abaqus.Odb.OdbStep.OdbStep` objects.
    sections: dict[str, Section]
        A repository of :py:class:`~abaqus.Section.Section.Section` objects.
    sectionCategories: dict[str, SectionCategory]
        A repository of :py:class:`~abaqus.Odb.SectionCategory.SectionCategory` objects.
    sectorDefinition: SectorDefinition
        A :py:class:`~abaqus.Odb.SectorDefinition.SectorDefinition` object.
    userData: UserData
        A :py:class:`~abaqus.Odb.UserData.UserData` object.
    customData: RepositorySupport
        A :py:class:`~abaqus.CustomKernel.RepositorySupport.RepositorySupport` object.
    profiles: dict[str, Profile]
        A repository of :py:class:`~abaqus.BeamSectionProfile.Profile.Profile` objects.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import odbAccess
        session.odbs[name]

    """

    def Part(self, name: str, embeddedSpace: SymbolicConstant, type: SymbolicConstant) -> OdbPart:
        """This method creates an OdbPart object. Nodes and elements are added to this object at a
        later stage.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                session.odbs[name].Part
        
        Parameters
        ----------
        name
            A String specifying the part name.
        embeddedSpace
            A SymbolicConstant specifying the dimensionality of the Part object. Possible values are
            THREE_D, TWO_D_PLANAR, and AXISYMMETRIC.
        type
            A SymbolicConstant specifying the type of the Part object. Possible values are
            DEFORMABLE_BODY and ANALYTIC_RIGID_SURFACE.

        Returns
        -------
            An OdbPart object.
        """
        self.parts[name] = odbPart = OdbPart(name, embeddedSpace, type)
        return odbPart

    def Step(self, name: str, description: str, domain: SymbolicConstant, timePeriod: float = 0,
             previousStepName: str = '', procedure: str = '', totalTime: float = None) -> OdbStep:
        """This method creates an OdbStep object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                session.odbs[name].Step
        
        Parameters
        ----------
        name
            A String specifying the repository key.
        description
            A String specifying the step description.
        domain
            A SymbolicConstant specifying the domain of the step. Possible values are TIME,
            FREQUENCY, ARC_LENGTH, and MODAL.The type of OdbFrame object that can be created for
            this step is based on the value of the *domain* argument.
        timePeriod
            A Float specifying the time period of the step. *timePeriod* is required if
            *domain*=TIME; otherwise, this argument is not applicable. The default value is 0.0.
        previousStepName
            A String specifying the preceding step. If *previousStepName* is the empty string, the
            last step in the repository is used. If *previousStepName* is not the last step, this
            will result in a change to the *previousStepName* member of the step that was in that
            position. A special value 'Initial' refers to the internal initial model step and may be
            used exclusively for inserting a new step at the first position before any other
            existing steps. The default value is an empty string.
        procedure
            A String specifying the step procedure. The default value is an empty string. The
            following is the list of valid procedures:
            ```
            *ANNEAL
            *BUCKLE
            *COMPLEX FREQUENCY
            *COUPLED TEMPERATURE-DISPLACEMENT
            *COUPLED TEMPERATURE-DISPLACEMENT, CETOL
            *COUPLED TEMPERATURE-DISPLACEMENT, STEADY STATE
            *COUPLED THERMAL-ELECTRICAL, STEADY STATE
            *COUPLED THERMAL-ELECTRICAL
            *COUPLED THERMAL-ELECTRICAL, DELTMX
            *DYNAMIC
            *DYNAMIC, DIRECT
            *DYNAMIC, EXPLICIT
            *DYNAMIC, SUBSPACE
            *DYNAMIC TEMPERATURE-DISPLACEMENT, EXPLICT
            *ELECTROMAGNETIC, HIGH FREQUENCY, TIME HARMONIC
            *ELECTROMAGNETIC, LOW FREQUENCY, TIME DOMAIN
            *ELECTROMAGNETIC, LOW FREQUENCY, TIME DOMAIN, DIRECT
            *ELECTROMAGNETIC, LOW FREQUENCY, TIME HARMONIC
            *FREQUENCY
            *GEOSTATIC
            *HEAT TRANSFER
            *HEAT TRANSFER, DELTAMX=__
            *HEAT TRANSFER, STEADY STATE
            *MAGNETOSTATIC
            *MAGNETOSTATIC, DIRECT
            *MASS DIFFUSION
            *MASS DIFFUSION, DCMAX=
            *MASS DIFFUSION, STEADY STATE
            *MODAL DYNAMIC
            *RANDOM RESPONSE
            *RESPONSE SPECTRUM
            *SOILS
            *SOILS, CETOL/UTOL
            *SOILS, CONSOLIDATION
            *SOILS, CONSOLIDATION, CETOL/UTOL
            *STATIC
            *STATIC, DIRECT
            *STATIC, RIKS
            *STEADY STATE DYNAMICS
            *STEADY STATE TRANSPORT
            *STEADY STATE TRANSPORT, DIRECT
            *STEP PERTURBATION, *STATIC
            *SUBSTRUCTURE GENERATE
            *USA ADDDED MASS GENERATION
            *VISCO
            ```
        totalTime
            A Float specifying the analysis time spend in all the steps previous to this step. The
            default value is −1.0.

        Returns
        -------
            An OdbStep object.

        Raises
        ------
            - If *previousStepName* is invalid:
              ValueError: previousStepName is invalid
        """
        self.steps[name] = odbStep = OdbStep(name, description, domain, timePeriod, previousStepName, procedure,
                                             totalTime)
        return odbStep

    def SectionCategory(self, name: str, description: str) -> SectionCategory:
        """This method creates a SectionCategory object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                session.odbs[*name*].SectionCategory
        
        Parameters
        ----------
        name
            A String specifying the name of the category.
        description
            A String specifying the description of the category.

        Returns
        -------
            A SectionCategory object.
        """
        self.sectionCategories[name] = sectionCategory = SectionCategory(name, description)
        return sectionCategory
