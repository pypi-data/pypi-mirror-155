from abaqusConstants import *


class Cell:
    """Cells are volumetric regions of geometry.

    Attributes
    ----------
    index: int
        An Int specifying the index of the cell in the CellArray.
    isReferenceRep: Boolean
        A Boolean specifying whether the cell belongs to the reference representation of the
        Part or Instance.
    pointOn: float
        A tuple of Floats specifying the **X**-, **Y**-, and **Z**-coordinates of a point located on
        the cell.
    featureName: float
        A tuple of Floats specifying the name of the feature that created this cell.
    instanceName: float
        A tuple of Floats specifying the name of the part instance for this cell (if
        applicable).

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import part
        mdb.models[name].parts[name].allInternalSets[name].cells[i]
        mdb.models[name].parts[name].allSets[name].cells[i]
        mdb.models[name].parts[name].cells[i]
        mdb.models[name].parts[name].sets[name].cells[i]
        import assembly
        mdb.models[name].rootAssembly.allInstances[name].cells[i]
        mdb.models[name].rootAssembly.allInstances[name].sets[name].cells[i]
        mdb.models[name].rootAssembly.allInternalSets[name].cells[i]
        mdb.models[name].rootAssembly.allSets[name].cells[i]
        mdb.models[name].rootAssembly.instances[name].cells[i]
        mdb.models[name].rootAssembly.instances[name].sets[name].cells[i]
        mdb.models[name].rootAssembly.modelInstances[i].sets[name].cells[i]
        mdb.models[name].rootAssembly.sets[name].cells[i]

    """

    # An Int specifying the index of the cell in the CellArray. 
    index: int = None

    # A Boolean specifying whether the cell belongs to the reference representation of the 
    # Part or Instance. 
    isReferenceRep: Boolean = OFF

    # A tuple of Floats specifying the *X*-, *Y*-, and *Z*-coordinates of a point located on 
    # the cell. 
    pointOn: float = None

    # A tuple of Floats specifying the name of the feature that created this cell. 
    featureName: float = None

    # A tuple of Floats specifying the name of the part instance for this cell (if 
    # applicable). 
    instanceName: float = None

    def getSize(self, printResults: Boolean = True):
        """This method returns a Float indicating the volume of the cell.
        
        Parameters
        ----------
        printResults
            A Boolean that determines whether a verbose output is to be printed. The default is 
            True. 

        Returns
        -------
            A Float.
            
        """
        pass

    def getFaces(self):
        """This method returns a sequence consisting of the face IDs of the faces which bound the
        cell.

        Returns
        -------
            A tuple of integers.
            
        """
        pass

    def getEdges(self):
        """This method returns a sequence consisting of the edge IDs of the edges on the cell.

        Returns
        -------
            A tuple of integers.
            
        """
        pass

    def getVertices(self):
        """This method returns a sequence consisting of the vertex IDs of the vertices on the cell.

        Returns
        -------
            A tuple of integers.
            
        """
        pass

    def getAdjacentCells(self):
        """This method returns an array of cell objects that share at least one face of the cell.

        Returns
        -------
            A CellArray object which is a sequence of Cell objects.
            
        """
        pass

    def getNodes(self):
        """This method returns an array of node objects that are associated with the cell.

        Returns
        -------
            A MeshNodeArray object which is a sequence of MeshNode objects.
            
        """
        pass

    def getElements(self):
        """This method returns an array of element objects that are associated with the cell.

        Returns
        -------
            A MeshElementArray object which is a sequence of MeshElement objects.
            
        """
        pass

    def getCADAttributes(self):
        """This method returns an array of CAD attribute strings associated with the cell when the
        part was created from CAD data.

        Returns
        -------
            An array of String.
            
        """
        pass
