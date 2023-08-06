from abaqusConstants import *
from .ConstrainedSketchDimension import ConstrainedSketchDimension
from ..ConstrainedSketchVertex.ConstrainedSketchVertex import ConstrainedSketchVertex


class ObliqueDimension(ConstrainedSketchDimension):

    def __init__(self, vertex1: ConstrainedSketchVertex, vertex2: ConstrainedSketchVertex,
                 textPoint: tuple[float], value: float = None, reference: Boolean = OFF):
        """This method constructs a ConstrainedSketchDimension object between two vertices. An
        oblique dimension indicates the distance between two vertices.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].ObliqueDimension
        
        Parameters
        ----------
        vertex1
            A ConstrainedSketchVertex object specifying the first endpoint. 
        vertex2
            A ConstrainedSketchVertex object specifying the second endpoint. 
        textPoint
            A pair of Floats specifying the location of the dimension text. 
        value
            A Float specifying the distance between the two ConstrainedSketchVertex objects. 
        reference
            A Boolean specifying whether the created dimension enforces the above value or if it 
            simply measures the distance between the two vertices. 

        Returns
        -------
            A ConstrainedSketchDimension object (None if the dimension cannot be created).
            
        """
        pass
