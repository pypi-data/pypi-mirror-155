from .Layer import Layer
from ..Annotation.AnnotationViewport import AnnotationViewport


class Viewport(AnnotationViewport):

    def Layer(self, name: str, copyViewName: str = '') -> Layer:
        """This method creates a Layer object in the Layer repository.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                session.viewports[name].Layer
        
        Parameters
        ----------
        name
            A String specifying the repository key.
        copyViewName
            A String specifying the name of the layer to copy.

        Returns
        -------
            A Layer object.
        """
        self.layers[name] = layer = Layer(name, copyViewName)
        return layer
