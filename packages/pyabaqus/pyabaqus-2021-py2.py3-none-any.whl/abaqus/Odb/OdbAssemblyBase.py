from abaqusConstants import *
from .OdbDatumCsys import OdbDatumCsys
from .OdbInstance import OdbInstance
from .OdbMeshElementArray import OdbMeshElementArray
from .OdbMeshNodeArray import OdbMeshNodeArray
from .OdbPretensionSectionArray import OdbPretensionSectionArray
from .OdbRigidBodyArray import OdbRigidBodyArray
from .OdbSet import OdbSet
from .SectionCategory import SectionCategory
from ..Assembly.ConnectorOrientationArray import ConnectorOrientationArray
from ..Property.SectionAssignmentArray import SectionAssignmentArray
from ..Section.Section import Section


class OdbAssemblyBase:
    """The OdbAssembly object has no constructor; it is created automatically when an Odb
    object is created. Abaqus creates the *rootAssembly* member when an Odb object is 
    created. 

    Attributes
    ----------
    instances: dict[str, OdbInstance]
        A repository of :py:class:`~abaqus.Odb.OdbInstance.OdbInstance` objects.
    nodeSets: dict[str, OdbSet]
        A repository of :py:class:`~abaqus.Odb.OdbSet.OdbSet` objects specifying node sets.
    elementSets: dict[str, OdbSet]
        A repository of :py:class:`~abaqus.Odb.OdbSet.OdbSet` objects specifying element sets.
    surfaces: dict[str, OdbSet]
        A repository of :py:class:`~abaqus.Odb.OdbSet.OdbSet` objects specifying surfaces.
    nodes: OdbMeshNodeArray
        An :py:class:`~abaqus.Odb.OdbMeshNodeArray.OdbMeshNodeArray` object.
    elements: OdbMeshElementArray
        An :py:class:`~abaqus.Odb.OdbMeshElementArray.OdbMeshElementArray` object.
    datumCsyses: dict[str, OdbDatumCsys]
        A repository of :py:class:`~abaqus.Odb.OdbDatumCsys.OdbDatumCsys` objects.
    sectionAssignments: SectionAssignmentArray
        A :py:class:`~abaqus.Property.SectionAssignmentArray.SectionAssignmentArray` object.
    rigidBodies: OdbRigidBodyArray
        An :py:class:`~abaqus.Odb.OdbRigidBodyArray.OdbRigidBodyArray` object.
    pretensionSections: OdbPretensionSectionArray
        An :py:class:`~abaqus.Odb.OdbPretensionSectionArray.OdbPretensionSectionArray` object.
    connectorOrientations: ConnectorOrientationArray
        A :py:class:`~abaqus.Assembly.ConnectorOrientationArray.ConnectorOrientationArray` object.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import odbAccess
        session.odbs[name].rootAssembly

    """

    # A repository of OdbInstance objects. 
    instances: dict[str, OdbInstance] = dict[str, OdbInstance]()

    # A repository of OdbSet objects specifying node sets. 
    nodeSets: dict[str, OdbSet] = dict[str, OdbSet]()

    # A repository of OdbSet objects specifying element sets. 
    elementSets: dict[str, OdbSet] = dict[str, OdbSet]()

    # A repository of OdbSet objects specifying surfaces. 
    surfaces: dict[str, OdbSet] = dict[str, OdbSet]()

    # An OdbMeshNodeArray object. 
    nodes: OdbMeshNodeArray = OdbMeshNodeArray()

    # An OdbMeshElementArray object. 
    elements: OdbMeshElementArray = OdbMeshElementArray()

    # A repository of OdbDatumCsys objects. 
    datumCsyses: dict[str, OdbDatumCsys] = dict[str, OdbDatumCsys]()

    # A SectionAssignmentArray object. 
    sectionAssignments: SectionAssignmentArray = SectionAssignmentArray()

    # An OdbRigidBodyArray object. 
    rigidBodies: OdbRigidBodyArray = OdbRigidBodyArray()

    # An OdbPretensionSectionArray object. 
    pretensionSections: OdbPretensionSectionArray = OdbPretensionSectionArray()

    # A ConnectorOrientationArray object. 
    connectorOrientations: ConnectorOrientationArray = ConnectorOrientationArray()

    def ConnectorOrientation(self, region: str, localCsys1: OdbDatumCsys = OdbDatumCsys(),
                             axis1: SymbolicConstant = AXIS_1, angle1: float = 0, orient2sameAs1: Boolean = OFF,
                             localCsys2: OdbDatumCsys = OdbDatumCsys(), axis2: SymbolicConstant = AXIS_1,
                             angle2: float = 0):
        """This method assigns a connector orientation to a connector region.
        
        Parameters
        ----------
        region
            An OdbSet specifying a region. 
        localCsys1
            An OdbDatumCsys object specifying the first connector node local coordinate system or 
            None, indicating the global coordinate system. 
        axis1
            A SymbolicConstant specifying the axis of a cylindrical or spherical datum coordinate 
            system about which an additional rotation of the first connector node is applied. 
            Possible values are AXIS_1, AXIS_2, and AXIS_3. The default value is AXIS_1. 
        angle1
            A Float specifying the angle of the additional rotation about the first connector node 
            axis. The default value is 0.0. 
        orient2sameAs1
            A Boolean specifying whether the same orientation settings should be used for the second 
            node of the connector. The default value is OFF. 
        localCsys2
            An OdbDatumCsys object specifying the second connector node local coordinate system or 
            None, indicating the global coordinate system. 
        axis2
            A SymbolicConstant specifying the axis of a cylindrical or spherical datum coordinate 
            system about which an additional rotation of the second connector node is applied. 
            Possible values are AXIS_1, AXIS_2, and AXIS_3. The default value is AXIS_1. 
        angle2
            A Float specifying the angle of the additional rotation about the second connector node 
            axis. The default value is 0.0.

        Raises
        ------
            - If *region* is not an element set: 
              OdbError: Connector orientation assignment requires element set. 
        """
        pass

    def SectionAssignment(self, region: str, section: Section):
        """This method is used to assign a section on an assembly or part. Section assignment on
        the assembly is limited to the connector elements only.
        
        Parameters
        ----------
        region
            An OdbSet specifying a region. 
        section
            A Section object.

        Raises
        ------
            - If *region* is not an element set: 
              OdbError: Section assignment requires element set. 
        """
        pass

    def addElements(self, labels: tuple, connectivity: tuple, instanceNames: tuple, type: str,
                    elementSetName: str = '', sectionCategory: SectionCategory = None):
        """This method is used to define elements using nodes defined at the OdbAssembly and/or
        OdbInstance level. For connector elements connected to ground, specify the lone node in
        the connectivity. The position of the ground node cannot be specified. This is a
        limitation.
        Warning:Adding elements not in ascending order of their labels may cause Abaqus/Viewer
        to plot contours incorrectly.
        
        Parameters
        ----------
        labels
            A sequence of Ints specifying the element labels. 
        connectivity
            A sequence of sequences of Ints specifying the nodal connectivity. 
        instanceNames
            A sequence of Strings specifying the instanceNames of each node in the nodal 
            connectivity array. If the node is defined at the assembly level, the instance name 
            should be an empty string 
        type
            A String specifying the element type. 
        elementSetName
            A String specifying a name for this element set. The default value is the empty string. 
        sectionCategory
            A SectionCategory object for this element set.

        Raises
        ------
            - Only certain element types are permitted at the assembly level. e.g., connector 
            elements. 
              OdbError: Addition of this element type is not permitted at the assembly level 
            - If length of label array does not match connectivity data length: 
              OdbError: Connectivity array must be provided for all element 
        """
        pass

    def addNodes(self, labels: tuple, coordinates: tuple, nodeSetName: str = None):
        """This method adds nodes to the OdbAssembly object using node labels and coordinates.
        Warning:Adding nodes not in ascending order of their labels may cause Abaqus/Viewer to
        plot contours incorrectly.
        
        Parameters
        ----------
        labels
            A sequence of Ints specifying the node labels. 
        coordinates
            A sequence of sequences of Floats specifying the nodal coordinates. 
        nodeSetName
            A String specifying a name for this node set. The default value is None.

        Raises
        ------
            - If length of labels does not match length of coordinates: 
              OdbError: Number of node labels and coordinates does not match 
            - If width of coordinate array does not match assembly dimension: 
              OdbError: Node location specification does not correspond to part dimensions 
        """
        pass

    def RigidBody(self, referenceNode: str, position: str = INPUT, isothermal: Boolean = OFF, elset: str = '',
                  pinNodes: str = '', tieNodes: str = '', analyticSurface: str = ''):
        """This method defines an OdbRigidBody on the assembly.
        
        Parameters
        ----------
        referenceNode
            An OdbSet specifying the reference node assigned to the rigid body. 
        position
            A symbolic constant specify if the location of the reference node is to be defined by 
            the user. Possible values are INPUT and CENTER_OF_MASS. The default value is INPUT. 
        isothermal
            A Boolean specifying an isothermal rigid body. The default value is OFF. This parameter 
            is used only for a fully coupled thermal stress analysis. 
        elset
            An OdbSet specifying an element set assigned to the rigid body. 
        pinNodes
            An OdbSet specifying pin-type nodes assigned to the rigid body. 
        tieNodes
            An OdbSet specifying tie-type nodes assigned to the rigid body. 
        analyticSurface
            An AnalyticSurface specifying the Analytic Rigid Surface assigned to the rigid body.

        Raises
        ------
            - If *referenceNode* is not a node set: 
              OdbError: Rigid body definition requires a node set. 
        """
        pass
