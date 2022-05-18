from framework.utilities import Asserts
from project.consts import PinsId, GearShifter, SignalsId, BrakePedal
from project.models import Pin, Signal


class VehicleSteps:
    """
    Class with Vehicle Steps functions
    """

    @staticmethod
    def set_gear_position(position: str):
        """
        Sets GearShifter position
        :param position(str): one of     Gear.Shifter.PARK, Gear.Shifter.NEUTRAL,
                                         Gear.Shifter.REVERSE, Gear.Shifter.DRIVE
        :return: None
        """
        gears = Pin.get_object([PinsId.GEAR_1, PinsId.GEAR_2])
        for index, gear in enumerate(gears):
            gear.update_object(voltage=GearShifter.STATES[position][index])

    @staticmethod
    def switch_gear_with_brake_pedal(gear_pos: str):
        """
        Releases brake pedal, switch gear, press brake pedal again
        :param gear_pos(str): one of PARK, NEUTRAL, REVERSE, DRIVE
        :return: None
        """
        Pin.get_object(PinsId.BRAKE_PEDAL).update_object(voltage=BrakePedal.STATES[BrakePedal.PRESSED])
        Asserts.assert_objects_equal(Signal.get_object(SignalsId.BRAKE_PEDAL).value, BrakePedal.PRESSED)
        VehicleSteps.set_gear_position(gear_pos)
        Asserts.assert_objects_equal(Signal.get_object(SignalsId.GEAR_POSITION).value, gear_pos)
        Pin.get_object(PinsId.BRAKE_PEDAL).update_object(voltage=BrakePedal.STATES[BrakePedal.RELEASED])
        Asserts.assert_objects_equal(Signal.get_object(SignalsId.BRAKE_PEDAL).value, BrakePedal.RELEASED)
