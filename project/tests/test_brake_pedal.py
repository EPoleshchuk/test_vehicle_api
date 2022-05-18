import pytest

from framework.utilities import Asserts
from project.consts import PinsId, SignalsId, GearShifter, BrakePedal, ReqTorque, AccPedal
from project.models import Pin, Signal
from project.utilities import VehicleUtils
from project.steps import VehicleSteps, CommonSteps


class TestBrakePedal:
    """
    Class with tests for Brake Pedal
    """

    @pytest.mark.parametrize("voltage", [0, 0.99, 1.01, 1.99, 2, 2.01, 2.99, 3, 3.01])
    def test_voltages(self, voltage):
        Pin.get_object(PinsId.BRAKE_PEDAL).update_object(voltage=voltage)
        Asserts.assert_objects_equal(Signal.get_object(SignalsId.BRAKE_PEDAL).value,
                                     VehicleUtils.get_brake_pedal_state_by_voltage(voltage),
                                     f"Voltage={voltage}, Brake Pedal value = {{}}, but {{}} expected")

    @pytest.mark.parametrize("acc_pedal_state",
                             [AccPedal.PERCENT_0, AccPedal.PERCENT_30, AccPedal.PERCENT_50, AccPedal.PERCENT_100])
    @pytest.mark.parametrize("start_gear_state", GearShifter.ALL_STATES)
    def test_pressed(self, acc_pedal_state, start_gear_state):
        Pin.get_object(PinsId.ACC_PEDAL).update_object(voltage=AccPedal.STATES[acc_pedal_state])
        Pin.get_object(PinsId.BRAKE_PEDAL).update_object(voltage=BrakePedal.STATES[BrakePedal.PRESSED])

        Asserts.assert_objects_equal(Signal.get_object(SignalsId.REQ_TORQUE).value, ReqTorque.NM_0,
                                     "Requested Torque did not drop. Current value = {}, but {} expected")
        CommonSteps.assert_switching_gear(set(GearShifter.ALL_STATES) - set(start_gear_state), expect_switching=True)

    @pytest.mark.parametrize("start_gear_state", GearShifter.ALL_STATES)
    @pytest.mark.parametrize("acc_pedal_state",
                             [AccPedal.PERCENT_0, AccPedal.PERCENT_30, AccPedal.PERCENT_50, AccPedal.PERCENT_100])
    def test_released(self, start_gear_state, acc_pedal_state):
        Pin.get_object(PinsId.BRAKE_PEDAL).update_object(voltage=BrakePedal.STATES[BrakePedal.RELEASED])
        VehicleSteps.set_gear_position(GearShifter.PARK)

        CommonSteps.assert_switching_gear([GearShifter.PARK, GearShifter.DRIVE, GearShifter.REVERSE],
                                          expect_switching=False)

        Pin.get_object(PinsId.ACC_PEDAL).update_object(voltage=AccPedal.STATES[acc_pedal_state])

        Asserts.assert_objects_equal(
            Signal.get_object(SignalsId.REQ_TORQUE).value,
            VehicleUtils.get_req_torque_by_percent(
                VehicleUtils.get_acc_pedal_pos_by_voltage(AccPedal.STATES[acc_pedal_state])),
            f"Voltage={AccPedal.STATES[acc_pedal_state]}, ReqTorque value={{}}, but {{}} expected")

    @pytest.mark.parametrize("start_gear_state", GearShifter.ALL_STATES)
    @pytest.mark.parametrize("acc_pedal_state",
                             [AccPedal.PERCENT_0, AccPedal.PERCENT_30, AccPedal.PERCENT_50, AccPedal.PERCENT_100])
    def test_error(self, start_gear_state, acc_pedal_state):
        VehicleSteps.set_gear_position(GearShifter.PARK)
        Pin.get_object(PinsId.ACC_PEDAL).update_object(voltage=AccPedal.STATES[acc_pedal_state])
        Pin.get_object(PinsId.BRAKE_PEDAL).update_object(voltage=BrakePedal.STATES[BrakePedal.ERROR])

        Asserts.assert_objects_equal(Signal.get_object(SignalsId.GEAR_POSITION).value, GearShifter.NEUTRAL,
                                     "GearPosition has not been switched. GearPosition = {}, but expected = {}")

        Asserts.assert_objects_equal(
            Signal.get_object(SignalsId.REQ_TORQUE).value, ReqTorque.NM_0,
            f"Voltage={AccPedal.STATES[acc_pedal_state]}, ReqTorque value={{}}, but {{}} expected")
