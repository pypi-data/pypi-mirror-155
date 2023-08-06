from .MeshElement import MeshElement


class MeshElementArray(list[MeshElement]):
    """The MeshElementArray is a sequence of MeshElement objects.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import part
        mdb.models[name].parts[name].allInternalSets[name].elements
        mdb.models[name].parts[name].allInternalSurfaces[name].elements
        mdb.models[name].parts[name].allSets[name].elements
        mdb.models[name].parts[name].allSurfaces[name].elements
        mdb.models[name].parts[name].elements
        mdb.models[name].parts[name].sets[name].elements
        mdb.models[name].parts[name].surfaces[name].elements
        import assembly
        mdb.models[name].rootAssembly.allInstances[name].elements
        mdb.models[name].rootAssembly.allInstances[name].sets[name].elements
        mdb.models[name].rootAssembly.allInstances[name].surfaces[name].elements
        mdb.models[name].rootAssembly.allInternalSets[name].elements
        mdb.models[name].rootAssembly.allInternalSurfaces[name].elements
        mdb.models[name].rootAssembly.allSets[name].elements
        mdb.models[name].rootAssembly.allSurfaces[name].elements
        mdb.models[name].rootAssembly.elements
        mdb.models[name].rootAssembly.instances[name].elements
        mdb.models[name].rootAssembly.instances[name].sets[name].elements
        mdb.models[name].rootAssembly.instances[name].surfaces[name].elements
        mdb.models[name].rootAssembly.modelInstances[i].elements
        mdb.models[name].rootAssembly.modelInstances[i].sets[name].elements
        mdb.models[name].rootAssembly.modelInstances[i].surfaces[name].elements
        mdb.models[name].rootAssembly.sets[name].elements
        mdb.models[name].rootAssembly.surfaces[name].elements

    """

    def __init__(self, elements: list[MeshElement]):
        """This method creates a MeshElementArray object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mesh.MeshElementArray
        
        Parameters
        ----------
        elements
            A list of MeshElement objects. 

        Returns
        -------
            A MeshElementArray object.
        """
        super().__init__()

    def getFromLabel(self, label: int):
        """This method returns the object in the MeshElementArray with the given label.
        
        Parameters
        ----------
        label
            An Int specifying the label of the object. 

        Returns
        -------
            A MeshElement object.
        """
        pass

    def getSequenceFromMask(self, mask: str):
        """This method returns the objects in the MeshElementArray identified using the specified
        *mask*. This command is generated when the JournalOptions are set to COMPRESSEDINDEX.
        When a large number of objects are involved, this method is highly efficient.
        
        Parameters
        ----------
        mask
            A String specifying the object or objects. 

        Returns
        -------
            A MeshElementArray object.
        """
        pass

    def getMask(self):
        """This method returns a string specifying the object or objects.

        Returns
        -------
            A String specifying the object or objects.
        """
        pass

    def getExteriorEdges(self):
        """This method returns the exterior element edges for 2D/shell elements in the
        MeshElementArray. These are edges referenced by exactly one element in the sequence.
        Nothing is returned if the sequence contains no topologically 2D/shell elements.

        Returns
        -------
            A MeshEdgeArray object specifying the element edges on the exterior.
        """
        pass

    def getExteriorFaces(self):
        """This method returns the exterior element faces for solid elements in the
        MeshElementArray. These are faces referenced by exactly one element in the sequence.
        Nothing is returned if the sequence contains no topologically solid elements.

        Returns
        -------
            A MeshFaceArray object specifying the element faces on the exterior.
        """
        pass

    def getByBoundingBox(self, xMin: str = '', yMin: str = '', zMin: str = '', xMax: str = '', yMax: str = '',
                         zMax: str = ''):
        """This method returns an array of element objects that lie within the specified bounding
        box.
        
        Parameters
        ----------
        xMin
            A float specifying the minimum X boundary of the bounding box. 
        yMin
            A float specifying the minimum Y boundary of the bounding box. 
        zMin
            A float specifying the minimum Z boundary of the bounding box. 
        xMax
            A float specifying the maximum X boundary of the bounding box. 
        yMax
            A float specifying the maximum Y boundary of the bounding box. 
        zMax
            A float specifying the maximum Z boundary of the bounding box. 

        Returns
        -------
            A MeshElementArray object, which is a sequence of MeshElement objects.
        """
        pass

    def getByBoundingCylinder(self, center1: tuple, center2: tuple, radius: str):
        """This method returns an array of element objects that lie within the specified bounding
        cylinder.
        
        Parameters
        ----------
        center1
            A tuple of the X-, Y-, and Z-coordinates of the center of the first end of the cylinder. 
        center2
            A tuple of the X-, Y-, and Z-coordinates of the center of the second end of the 
            cylinder. 
        radius
            A float specifying the radius of the cylinder. 

        Returns
        -------
            A MeshElementArray object, which is a sequence of MeshElement objects.
        """
        pass

    def getByBoundingSphere(self, center: tuple, radius: str):
        """This method returns an array of element objects that lie within the specified bounding
        sphere.
        
        Parameters
        ----------
        center
            A tuple of the X-, Y-, and Z-coordinates of the center of the sphere. 
        radius
            A float specifying the radius of the sphere. 

        Returns
        -------
            A MeshElementArray object, which is a sequence of MeshElement objects.
        """
        pass

    def getBoundingBox(self):
        """This method returns a dictionary of two tuples representing minimum and maximum boundary
        values of the bounding box of the minimum size containing the element sequence.

        Returns
        -------
            A Dictionary object with the following items: 
            *low*: a tuple of three floats representing the minimum x, y, and z boundary values of 
            the bounding box. 
            *high*: a tuple of three floats representing the maximum x, y, and z boundary values of 
            the bounding box.
        """
        pass

    def sequenceFromLabels(self, labels: tuple):
        """This method returns the objects in the MeshElementArray identified using the specified
        labels.
        
        Parameters
        ----------
        labels
            A sequence of Ints specifying the labels. 

        Returns
        -------
            A MeshElementArray object. 

        Raises
        ------
            - An exception occurs if the resulting sequence is empty. 
              Error: The mask results in an empty sequence 
        """
        pass
