import pytest

from project.consts import PinsId, SignalsId, BrakePedal, ReqTorque, AccPedal, GearShifter
from project.models import Pin, Signal
from project.utilities import VehicleUtils
from project.steps import VehicleSteps
from framework.utilities import Asserts


class TestAccPedalAndReqTorque:
    """
    Class with tests for AccPedal and ReqTorque
    """

    @pytest.mark.parametrize("voltage", [0.99, 1, 1.01, 1.99, 2, 2.01, 2.49, 2.51, 2.99, 3, 3.01, 3.49, 3.5, 3.51])
    def test_voltages(self, voltage):
        Pin.get_object(PinsId.ACC_PEDAL).update_object(voltage=voltage)
        Asserts.assert_objects_equal(Signal.get_object(SignalsId.ACC_PEDAL).value,
                                     VehicleUtils.get_acc_pedal_pos_by_voltage(voltage),
                                     f"Voltage={voltage}, AccPedal value={{}}, but {{}} expected")

    @pytest.mark.parametrize("acc_pedal_state", [AccPedal.PERCENT_0, AccPedal.ERROR])
    def test_with_acc_with_error_brake_pedal(self, acc_pedal_state):
        Pin.get_object(PinsId.ACC_PEDAL).update_object(voltage=AccPedal.STATES[acc_pedal_state])
        Pin.get_object(PinsId.BRAKE_PEDAL).update_object(voltage=BrakePedal.ERROR)
        Asserts.assert_objects_equal(Signal.get_object(SignalsId.REQ_TORQUE).value, ReqTorque.NM_0,
                                     "Requested Torque={}, but {} expected")

    @pytest.mark.parametrize("acc_pedal_state", [AccPedal.PERCENT_30, AccPedal.PERCENT_50, AccPedal.PERCENT_100])
    @pytest.mark.parametrize("gear_state", [GearShifter.DRIVE, GearShifter.REVERSE])
    def test_with_pressed_brake_pedal(self, acc_pedal_state, gear_state):
        Pin.get_object(PinsId.ACC_PEDAL).update_object(voltage=AccPedal.STATES[acc_pedal_state])
        Pin.get_object(PinsId.BRAKE_PEDAL).update_object(voltage=BrakePedal.PRESSED)
        VehicleSteps.set_gear_position(gear_state)
        Asserts.assert_objects_equal(Signal.get_object(SignalsId.REQ_TORQUE).value, ReqTorque.NM_0,
                                     "Requested Torque = {}, but {} expected")

    @pytest.mark.parametrize("acc_pedal_state", [AccPedal.PERCENT_30, AccPedal.PERCENT_50, AccPedal.PERCENT_100])
    @pytest.mark.parametrize("gear_state", [GearShifter.DRIVE, GearShifter.REVERSE])
    def test_with_released_brake_pedal(self, acc_pedal_state, gear_state):
        Pin.get_object(PinsId.ACC_PEDAL).update_object(voltage=AccPedal.STATES[acc_pedal_state])
        Pin.get_object(PinsId.BRAKE_PEDAL).update_object(voltage=BrakePedal.RELEASED)
        VehicleSteps.set_gear_position(gear_state)

        Asserts.assert_objects_not_equal(VehicleUtils.get_req_torque_by_percent(acc_pedal_state),
                                         ReqTorque.NM_0, "Requested Torque value={}, but expected != {}")
