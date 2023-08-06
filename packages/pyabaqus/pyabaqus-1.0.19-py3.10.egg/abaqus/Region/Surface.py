import typing

from abaqusConstants import *
from ..BasicGeometry.EdgeArray import EdgeArray
from ..BasicGeometry.Face import Face
from ..BasicGeometry.FaceArray import FaceArray
from ..Mesh.MeshElementArray import MeshElementArray
from ..Mesh.MeshNodeArray import MeshNodeArray


class Surface:
    """The Surface object stores surfaces selected from the assembly. A surface is comprised of
    geometric or discrete entities but not both. An instance of a Surface object is 
    available from the *surface* member of the Assembly object. 

    Attributes
    ----------
    edges: EdgeArray
        An :py:class:`~abaqus.BasicGeometry.EdgeArray.EdgeArray` object.
    faces: FaceArray
        A :py:class:`~abaqus.BasicGeometry.FaceArray.FaceArray` object.
    elements: MeshElementArray
        A :py:class:`~abaqus.Mesh.MeshElementArray.MeshElementArray` object.
    nodes: MeshNodeArray
        A :py:class:`~abaqus.Mesh.MeshNodeArray.MeshNodeArray` object.
    sides: SymbolicConstant
        A tuple of SymbolicConstants specifying the sides; for example, (SIDE1, SIDE2).
    instances: int
        A tuple of Ints specifying the instances. This member is not applicable for a Surface
        object on an output database.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import part
        mdb.models[name].parts[name].allInternalSurfaces[name]
        mdb.models[name].parts[name].allSurfaces[name]
        mdb.models[name].parts[name].surfaces[name]
        import assembly
        mdb.models[name].rootAssembly.allInstances[name].surfaces[name]
        mdb.models[name].rootAssembly.allInternalSurfaces[name]
        mdb.models[name].rootAssembly.allSurfaces[name]
        mdb.models[name].rootAssembly.instances[name].surfaces[name]
        mdb.models[name].rootAssembly.modelInstances[i].surfaces[name]
        mdb.models[name].rootAssembly.surfaces[name]

    """

    # An EdgeArray object. 
    edges: EdgeArray = EdgeArray([])

    # A FaceArray object. 
    faces: FaceArray = FaceArray([])

    # A MeshElementArray object. 
    elements: MeshElementArray = MeshElementArray([])

    # A MeshNodeArray object. 
    nodes: MeshNodeArray = MeshNodeArray([])

    # A tuple of SymbolicConstants specifying the sides; for example, (SIDE1, SIDE2). 
    sides: SymbolicConstant = None

    # A tuple of Ints specifying the instances. This member is not applicable for a Surface 
    # object on an output database. 
    instances: int = None

    @typing.overload
    def __init__(self, side1Faces: tuple[Face] = None, side2Faces: tuple[Face] = None, side12Faces: tuple[Face] = None,
                 end1Edges: tuple[Face] = None, end2Edges: tuple[Face] = None, circumEdges: tuple[Face] = None,
                 side1Edges: tuple[Face] = None, side2Edges: tuple[Face] = None, face1Elements: tuple[Face] = None,
                 face2Elements: tuple[Face] = None, face3Elements: tuple[Face] = None,
                 face4Elements: tuple[Face] = None,
                 face5Elements: tuple[Face] = None, face6Elements: tuple[Face] = None,
                 side1Elements: tuple[Face] = None,
                 side2Elements: tuple[Face] = None, side12Elements: tuple[Face] = None,
                 end1Elements: tuple[Face] = None,
                 end2Elements: tuple[Face] = None, circumElements: tuple[Face] = None, name: str = '', **kwargs):
        """This method creates a surface from a sequence of objects in a model database. The
        surface will apply to the sides specified by the arguments.For example
        surface=mdb.models['Model-1'].parts['Part-1'].Surface(side1Faces=side1Faces,
        name='Surf-1')

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].parts[*name*].Surface
            mdb.models[name].rootAssembly.Surface
        kwargs

            On three-dimensional solid faces, you can use the following arguments:

            side1Faces
            side2Faces

            On three-dimensional shell faces, you can use the following arguments:

            side1Faces
            side2Faces
            side12Faces

            On three-dimensional wire edges, you can use the following arguments:

            end1Edges
            end2Edges
            circumEdges

            On three-dimensional or two-dimensional or axisymmetric edges, you can use the following arguments:

            side1Edges
            side2Edges

            On two-dimensional or axisymmetric shell elements, you can use the following arguments:

            face1Elements
            face2Elements
            face3Elements
            face4Elements

            On solid elements, you can use the following arguments:

            face1Elements
            face2Elements
            face3Elements
            face4Elements
            face5Elements
            face6Elements

            On three-dimensional shell elements, you can use the following arguments:

            side1Elements
            side2Elements
            side12Elements

            On three-dimensional wire elements, you can use the following arguments:

            end1Elements
            end2Elements
            circumElements

            On two-dimensional or axisymmetric wire elements, you can use the following arguments:

            side1Elements
            side2Elements

        
        Parameters
        ----------
        name
            A String specifying the repository key. The default value is an empty string. 

        Returns
        -------
            A Surface object.
        """
        pass

    @typing.overload
    def __init__(self, name: str, objectToCopy: 'Surface'):
        """This method copies a surface from an existing surface.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].parts[*name*].Surface
            mdb.models[name].rootAssembly.Surface
        
        Parameters
        ----------
        name
            A String specifying the name of the surface. 
        objectToCopy
            A Surface object to be copied. 

        Returns
        -------
            A Surface object.
        """
        pass

    def __init__(self, *args, **kwargs):
        pass

    def SurfaceByBoolean(self, name: str, surfaces: tuple['Surface'], operation: SymbolicConstant = UNION):
        """This method creates a surface by performing a boolean operation on two or more input
        surfaces.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].parts[*name*].Surface
            mdb.models[name].rootAssembly.Surface
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        surfaces
            A sequence of Surface objects. 
        operation
            A SymbolicConstant specifying the boolean operation to perform. Possible values are 
            UNION, INTERSECTION, andDIFFERENCE. The default value is UNION. Note that if DIFFERENCE 
            is specified, the order of the given input surfaces is important; All surfaces specified 
            after the first one are subtracted from the first one. 

        Returns
        -------
            A Surface object.
        """
        pass

    def SurfaceFromElsets(self, name: str, elementSetSeq: tuple):
        """This method creates a surface from a sequence of element sets in a model database.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].parts[*name*].Surface
            mdb.models[name].rootAssembly.Surface
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        elementSetSeq
            A sequence of element sets. For example,`elementSetSeq=((elset1, S1),(elset2, S2))`where 
            `elset1=mdb.models[name].rootAssembly.sets['Clutch']` and `S1` and `S2` indicate the 
            side of the element set. 

        Returns
        -------
            A Surface object.
        """
        pass
