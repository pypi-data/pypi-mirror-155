from abaqusConstants import *
from .ConstrainedSketchDimension import ConstrainedSketchDimension
from ..ConstrainedSketchVertex.ConstrainedSketchVertex import ConstrainedSketchVertex


class HorizontalDimension(ConstrainedSketchDimension):

    def __init__(self, vertex1: ConstrainedSketchVertex, vertex2: ConstrainedSketchVertex,
                 textPoint: tuple[float], value: float = None, reference: Boolean = OFF):
        """This method constructs a ConstrainedSketchDimension object between two vertices. A
        horizontal dimension indicates the horizontal distance along the *X*-axis between two
        vertices.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].HorizontalDimension
        
        Parameters
        ----------
        vertex1
            A ConstrainedSketchVertex object specifying the first endpoint. 
        vertex2
            A ConstrainedSketchVertex object specifying the second endpoint. 
        textPoint
            A pair of Floats specifying the location of the dimension text. 
        value
            A Float distance between the two vertices. 
        reference
            A Boolean specifying whether the created dimension enforces the above value or if it 
            simply measures the distance between the two vertices. 

        Returns
        -------
            A ConstrainedSketchDimension object (None if the dimension cannot be created).
            
        """
        pass
