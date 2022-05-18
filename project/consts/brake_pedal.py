class BrakePedal:
    """
    Class with BrakePedal constants
    """
    ERROR = "Error"
    PRESSED = "Pressed"
    RELEASED = "Released"

    ALL_STATES = [ERROR, PRESSED, RELEASED]
    STATES = dict(zip(ALL_STATES, [0, 1.5, 2.5]))
