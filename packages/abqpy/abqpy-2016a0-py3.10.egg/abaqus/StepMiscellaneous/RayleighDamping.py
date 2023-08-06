from .RayleighDampingComponentArray import RayleighDampingComponentArray


class RayleighDamping:
    """A :py:class:`~abaqus.StepMiscellaneous.RayleighDamping.RayleighDamping` object contains Rayleigh Damping parameters.

    Attributes
    ----------
    components: RayleighDampingComponentArray
        A :py:class:`~abaqus.StepMiscellaneous.RayleighDampingComponentArray.RayleighDampingComponentArray` object.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import step
        mdb.models[name].steps[name].rayleighDamping
    """

    # A :py:class:`~abaqus.StepMiscellaneous.RayleighDampingComponentArray.RayleighDampingComponentArray` object.
    components: RayleighDampingComponentArray = RayleighDampingComponentArray()
