from abaqusConstants import *
from ..Region.Region import Region


class ElementProgressiveActivation:
    """The ElementProgressiveActivation object is used to specify elements that can be
    activated during an analysis. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        mdb.models[name].rootAssembly.elementProgressiveActivations[name]

    The corresponding analysis keywords are:

    - *ELEMENT PROGRESSIVE ACTIVATION

    """

    def __init__(self, name: str, elset: Region = Region(), deformation: Boolean = OFF,
                 freeSurfaceType: SymbolicConstant = NONE):
        """This method creates an ElementProgressiveActivation object and places it in the
        elementProgressiveActivation repository.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].rootAssembly.ElementProgressiveActivation
        
        Parameters
        ----------
        name
            A String specifying the key of the repository. 
        elset
            A Region object specifying the region containing the elements that will be activated 
            during the analysis. 
        deformation
            A Boolean value specifying whether the elements that have not yet been activated will 
            follow the deformations of the active elements. Set *deformation*=ON when the 
            deformation of the active elements is excessive. The default value is OFF. 
        freeSurfaceType
            A SymbolicConstant specifying the exposed areas of the element facets that are active 
            for convection or radiation boundary conditions to be applied. Possible values are NONE 
            and FACET. If *freeSurfaceType*=FACET, user subroutine UEPACTIVATIONFACET will be called 
            at the start of the increment for each element. If *freeSurfaceType*=NONE, all the 
            exposed areas of the element facets are considered. The default value is NONE. 

        Returns
        -------
            An ElementProgressiveActivation object. 

        Raises
        ------
            AbaqusException: If the region does not contain only elements. 
        """
        pass

    def setValue(self):
        """The method modifies the ElementProgressiveActivation object.

        Returns
        -------

        Raises
        ------
        """
        pass
