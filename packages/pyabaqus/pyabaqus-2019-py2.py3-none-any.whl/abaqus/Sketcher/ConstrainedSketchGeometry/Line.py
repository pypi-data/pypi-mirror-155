from .ConstrainedSketchGeometry import ConstrainedSketchGeometry


class Line(ConstrainedSketchGeometry):

    def __init__(self, point1: tuple[float], point2: tuple[float]):
        """This method creates a line between two given points.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].Line
        
        Parameters
        ----------
        point1
            A pair of Floats specifying the first endpoint. 
        point2
            A pair of Floats specifying the second endpoint. 

        Returns
        -------
            A ConstrainedSketchGeometry object (None if the line cannot be created).
            
        """
        pass
