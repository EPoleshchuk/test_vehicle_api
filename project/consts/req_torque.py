from project.consts import AccPedal


class ReqTorque:
    """
    Class with ReqTorque constants
    """
    NM_0 = "0 Nm"
    NM_3000 = "3000 Nm"
    NM_5000 = "5000 Nm"
    NM_10000 = "10000 Nm"

    ALL_STATES = [NM_0, NM_3000, NM_5000, NM_10000]
    STATES = dict(zip([NM_0, *ALL_STATES], AccPedal.ALL_STATES))
