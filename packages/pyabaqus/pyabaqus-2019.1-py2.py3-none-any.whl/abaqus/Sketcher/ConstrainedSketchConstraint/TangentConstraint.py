from .ConstrainedSketchConstraint import ConstrainedSketchConstraint
from ..ConstrainedSketchGeometry.ConstrainedSketchGeometry import ConstrainedSketchGeometry


class TangentConstraint(ConstrainedSketchConstraint):

    def __init__(self, entity1: ConstrainedSketchGeometry, entity2: ConstrainedSketchGeometry):
        """This method creates a tangent constraint. This constraint applies to different types of
        ConstrainedSketchGeometry objects and constrains them to remain tangential.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].TangentConstraint
        
        Parameters
        ----------
        entity1
            A ConstrainedSketchGeometry object specifying the first object. 
        entity2
            A ConstrainedSketchGeometry object specifying the second object. 

        Returns
        -------
            A ConstrainedSketchConstraint object.
            
        """
        pass
