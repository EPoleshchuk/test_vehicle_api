import pytest

from framework.utilities import Asserts
from project.consts import PinsId, SignalsId, Battery, GearShifter, BrakePedal, AccPedal
from project.models import Pin, Signal
from project.steps import CommonSteps, VehicleSteps
from project.utilities import VehicleUtils


class TestBattery:
    """
    Class with tests for Battery
    """

    @pytest.mark.parametrize("voltage", [0, 0.01, 399.99, 400, 400.01, 799.99, 800, 800.01])
    def test_voltages(self, voltage):
        Pin.get_object(PinsId.BATTERY).update_object(voltage=voltage)
        Asserts.assert_objects_equal(Signal.get_object(SignalsId.BATTERY).value,
                                     VehicleUtils.get_battery_state_by_voltage(voltage),
                                     f"Voltage={voltage}, Battery value={{}}, but {{}} expected")

    def test_error_state(self):
        Pin.get_object(PinsId.BATTERY).update_object(voltage=Battery.STATES[Battery.ERROR])
        fields = ("gear_position", "gear_1", "gear_2", "brake_pedal_state", "brake_pedal_pos",
                  "acc_pedal_pos", "acc_pedal", "req_torque")
        expected_result = dict(zip(fields, (GearShifter.NEUTRAL, "0.0", "0.0",
                                            BrakePedal.ERROR, "0.0", AccPedal.ERROR, "0.0", "0 Nm")))
        received_result = dict(zip(fields, (Signal.get_object(SignalsId.GEAR_POSITION).value,
                                            Pin.get_object(PinsId.GEAR_1).voltage,
                                            Pin.get_object(PinsId.GEAR_2).voltage,
                                            Signal.get_object(SignalsId.BRAKE_PEDAL).value,
                                            Pin.get_object(PinsId.BRAKE_PEDAL).voltage,
                                            Signal.get_object(SignalsId.ACC_PEDAL).value,
                                            Pin.get_object(PinsId.ACC_PEDAL).voltage,
                                            Signal.get_object(SignalsId.REQ_TORQUE).value)))
        Asserts.soft_assert(received_result, expected_result)

    @pytest.mark.parametrize("start_gear_state", GearShifter.ALL_STATES)
    def test_not_ready_state(self, start_gear_state):
        VehicleSteps.set_gear_position(start_gear_state)
        Pin.get_object(PinsId.ACC_PEDAL).update_object(voltage=AccPedal.STATES[AccPedal.PERCENT_50])
        Pin.get_object(PinsId.BATTERY).update_object(voltage=Battery.STATES[Battery.NOT_READY])

        Asserts.assert_objects_equal(Signal.get_object(SignalsId.GEAR_POSITION).value, GearShifter.NEUTRAL,
                                     "Gear position has not been switched. GearPosition={}, but expected={}")
        CommonSteps.assert_switching_gear(set(GearShifter.ALL_STATES) - set(start_gear_state), expect_switching=False)
