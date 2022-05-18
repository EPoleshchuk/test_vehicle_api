class GearShifter:
    """
    Class with GearShifter constants
    """
    PARK = "Park"
    NEUTRAL = "Neutral"
    REVERSE = "Reverse"
    DRIVE = "Drive"

    ALL_STATES = [PARK, NEUTRAL, REVERSE, DRIVE]
    STATES = dict(zip(ALL_STATES, [(0.67, 3.12), (1.48, 2.28), (2.28, 1.48), (3.12, 0.67)]))
    