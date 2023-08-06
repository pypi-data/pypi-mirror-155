from .ConstrainedSketchConstraint import ConstrainedSketchConstraint
from ..ConstrainedSketchGeometry.ConstrainedSketchGeometry import ConstrainedSketchGeometry


class CoincidentConstraint(ConstrainedSketchConstraint):

    def __init__(self, entity1: ConstrainedSketchGeometry, entity2: ConstrainedSketchGeometry):
        """This method creates a coincident constraint. This constraint applies to two vertices, to
        a vertex and a ConstrainedSketchGeometry object, or to two ConstrainedSketchGeometry
        objects of the same type and constrains them to be coincident.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].CoincidentConstraint
        
        Parameters
        ----------
        entity1
            A ConstrainedSketchGeometry object or a ConstrainedSketchVertex object specifying the first object.
        entity2
            A ConstrainedSketchGeometry object or a ConstrainedSketchVertex object specifying the second object.

        Returns
        -------
            A ConstrainedSketchConstraint object.
            
        """
        pass
