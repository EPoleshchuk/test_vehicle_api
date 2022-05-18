class AccPedal:
    """
    Class with AccPedal constants
    """
    ERROR = "Error"
    PERCENT_0 = "0 %"
    PERCENT_30 = "30 %"
    PERCENT_50 = "50 %"
    PERCENT_100 = "100 %"

    ALL_STATES = [ERROR, PERCENT_0, PERCENT_30, PERCENT_50, PERCENT_100]
    STATES = dict(zip(ALL_STATES, [0, 1, 2, 2.5, 3]))
