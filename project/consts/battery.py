class Battery:
    """
    Class with Battery constants
    """
    READY = "Ready"
    NOT_READY = "NotReady"
    ERROR = "Error"

    ALL_STATES = [READY, NOT_READY, ERROR]
    STATES = dict(zip(ALL_STATES, [500, 200, 0]))