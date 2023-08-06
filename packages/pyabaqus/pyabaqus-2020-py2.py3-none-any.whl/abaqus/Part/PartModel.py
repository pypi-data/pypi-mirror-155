from abaqusConstants import *
from ..Model.ModelBase import ModelBase
from ..Part.Part import Part


class PartModel(ModelBase):
    """Abaqus creates a Model object named `Model-1` when a session is started.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        mdb.models[name]

    """

    def Part(self, name: str, dimensionality: SymbolicConstant, type: SymbolicConstant,
             twist: Boolean = OFF):
        """This method creates a Part object and places it in the parts repository.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].Part
        
        Parameters
        ----------
        name
            A String specifying the repository key.
        dimensionality
            A SymbolicConstant specifying the dimensionality of the part. Possible values are
            THREE_D, TWO_D_PLANAR, and AXISYMMETRIC.
        type
            A SymbolicConstant specifying the type of the part. Possible values are DEFORMABLE_BODY,
            EULERIAN, DISCRETE_RIGID_SURFACE, and ANALYTIC_RIGID_SURFACE.
        twist
            A Boolean specifying whether to include a twist DEGREE OF FREEDOM in the part (only
            available when *dimensionality*=AXISYMMETRIC and *type*=DEFORMABLE_BODY). The default
            value is OFF.

        Returns
        -------
            A Part object.
        """
        self.parts[name] = part = Part(name, dimensionality, type, twist)
        return part
