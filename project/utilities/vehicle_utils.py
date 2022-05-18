from project.consts import Battery, BrakePedal, AccPedal, ReqTorque


class VehicleUtils:
    """
    Class with Vehicle utilities
    """

    @staticmethod
    def get_battery_state_by_voltage(voltage: int) -> str:
        """
        Returns Battery state by voltage
        :param voltage(int): Battery voltage
        :return(str): Battery state
        """
        if 800 >= voltage > 400:
            return Battery.READY
        elif 0 < voltage <= 400:
            return Battery.NOT_READY
        else:
            return Battery.ERROR

    @staticmethod
    def get_brake_pedal_state_by_voltage(voltage: int) -> str:
        """
        Returns Brake pedal state by voltage
        :param voltage(int): Brake pedal voltage
        :return(str): Brake pedal state
        """
        if 1 <= voltage < 2:
            return BrakePedal.PRESSED
        elif 2 <= voltage < 3:
            return BrakePedal.RELEASED
        else:
            return BrakePedal.ERROR

    @staticmethod
    def get_acc_pedal_pos_by_voltage(voltage: int) -> str:
        """
        Returns Acc pedal position by voltage
        :param voltage(int): Acc pedal position
        :return(str): Acc pedal position
        """
        if 1 <= voltage < 2:
            return AccPedal.PERCENT_0
        elif 2 <= voltage < 2.5:
            return AccPedal.PERCENT_30
        elif 2.5 <= voltage < 3:
            return AccPedal.PERCENT_50
        elif 3 <= voltage < 3.5:
            return AccPedal.PERCENT_100
        else:
            return AccPedal.ERROR

    @staticmethod
    def get_req_torque_by_percent(percent: str) -> str:
        """
        Returns Req Torque value by percent
        :param percent(str): Acc pedal pos
        :return(str): Req Torque value
        """
        return dict(zip(list(ReqTorque.STATES.values()), list(ReqTorque.STATES.keys())))[percent]
