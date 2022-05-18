from typing import Iterable

from framework.utilities import Asserts
from project.consts import SignalsId
from project.models import Signal
from project.steps import VehicleSteps
from project.utilities import VehicleUtils


class CommonSteps:
    """
    Class with Common steps functions
    """

    @staticmethod
    def assert_switching_gear(gears_list: Iterable[str], expect_switching: bool = True):
        """
        Assert switching or not Gear position for each gear_pos in gears_list
        :param gears_list(iterable): list of gear positions to switching over then
        :param expect_switching(optional, bool): Should Gear position switch or not
        :raises: AssertionError when gear switched but not expect or vice versa
        :return: None
        """
        start_gear_pos = Signal.get_object(SignalsId.GEAR_POSITION).value
        assert_message = "GearPosition has not been switched. GearPosition = {}, but expected = {}" \
            if expect_switching else "GearPosition has been switched. GearPosition = {}, but expected = {}"
        assert_errors = []
        for gear_pos in gears_list:
            VehicleSteps.set_gear_position(gear_pos)
            current_position = Signal.get_object(SignalsId.GEAR_POSITION).value
            if expect_switching and current_position != gear_pos or \
                    not expect_switching and current_position != start_gear_pos:
                assert_errors.append(assert_message.format(current_position,
                                                           gear_pos if expect_switching else start_gear_pos))

        if assert_errors:
            raise AssertionError("\n".join(assert_errors))

    @staticmethod
    def assert_acc_pedal_and_req_torque(acc_pedal_pos: str):
        """
        Assert Acc Pedal pos and ReqTorque value
        :param acc_pedal_pos(str): one of ERROR, PERCENT_0, PERCENT_30, PERCENT_50, PERCENT_100
        :raises: AssertionError if ReqTorqueValue != ReqTorqueValue in acc_pedal_pos
                                the same with AccPedalPos
        :return: None
        """
        Asserts.assert_objects_equal(Signal.get_object(SignalsId.REQ_TORQUE).value,
                                     VehicleUtils.get_req_torque_by_percent(acc_pedal_pos))
        Asserts.assert_objects_equal(Signal.get_object(SignalsId.ACC_PEDAL).value, acc_pedal_pos)
