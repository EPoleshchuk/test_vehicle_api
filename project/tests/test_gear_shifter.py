import pytest

from project.consts import PinsId, SignalsId, GearShifter, BrakePedal, AccPedal, Battery
from project.models import Pin, Signal
from project.steps import VehicleSteps


class TestGearShifter:
    """
    Class with tests for Gear Shifter
    """
    @pytest.mark.parametrize("start_gear_state", GearShifter.ALL_STATES)
    def test_gear_switch_with_correct_data(self, start_gear_state):
        Pin.get_object(PinsId.BRAKE_PEDAL).update_object(voltage=BrakePedal.PRESSED)

        assert_message = "GearPosition has not been switched. GearPosition = {}, but expected = {}"
        for gear_state in set(GearShifter.ALL_STATES) - set(start_gear_state):
            VehicleSteps.set_gear_position(gear_state)
            gear_position = Signal.get_object(SignalsId.GEAR_POSITION).value
            assert gear_position == gear_state, assert_message.format(gear_position, gear_state)

    @pytest.mark.parametrize("brake_pedal_state", [BrakePedal.RELEASED, BrakePedal.ERROR])
    @pytest.mark.parametrize("gear_state", [GearShifter.DRIVE, GearShifter.REVERSE, GearShifter.PARK])
    def test_gear_switch_with_incorrect_brake_pedal_state(self, brake_pedal_state, gear_state):
        Pin.get_object(PinsId.BRAKE_PEDAL).update_object(voltage=brake_pedal_state)

        assert_message = "GearPosition has been switched. GearPosition = {}, but expected = {}"
        VehicleSteps.set_gear_position(gear_state)
        gear_position = Signal.get_object(SignalsId.GEAR_POSITION).value
        assert gear_position == GearShifter.NEUTRAL, assert_message.format(gear_position, GearShifter.NEUTRAL)

    @pytest.mark.parametrize("acc_pedal_state", [AccPedal.PERCENT_30, AccPedal.PERCENT_50, AccPedal.PERCENT_100])
    @pytest.mark.parametrize("gear_state", [GearShifter.DRIVE, GearShifter.REVERSE, GearShifter.PARK])
    def test_gear_switch_with_incorrect_acc_pedal_state(self, acc_pedal_state, gear_state):
        Pin.get_object(PinsId.ACC_PEDAL).update_object(voltage=AccPedal.STATES[acc_pedal_state])

        assert_message = "GearPosition has been switched. GearPosition = {}, but expected = {}"
        VehicleSteps.set_gear_position(gear_state)
        gear_position = Signal.get_object(SignalsId.GEAR_POSITION).value
        assert gear_position == GearShifter.NEUTRAL, assert_message.format(gear_position, GearShifter.NEUTRAL)

    @pytest.mark.parametrize("battery_state", [Battery.NOT_READY, Battery.ERROR])
    @pytest.mark.parametrize("gear_state", [GearShifter.DRIVE, GearShifter.REVERSE, GearShifter.PARK])
    def test_gear_switch_with_incorrect_battery_state(self, battery_state, gear_state):
        Pin.get_object(PinsId.BATTERY).update_object(voltage=Battery.STATES[battery_state])

        assert_message = "GearPosition has been switched. GearPosition = {}, but expected = {}"
        VehicleSteps.set_gear_position(gear_state)
        gear_position = Signal.get_object(SignalsId.GEAR_POSITION).value
        assert gear_position == GearShifter.NEUTRAL, assert_message.format(gear_position, GearShifter.NEUTRAL)
