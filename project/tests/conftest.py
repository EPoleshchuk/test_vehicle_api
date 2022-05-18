import pytest

from project.consts import GearShifter, PinsId, AccPedal, BrakePedal, Battery
from project.models import Pin
from project.steps import VehicleSteps


@pytest.fixture(scope="function", autouse=True)
def set_default_system_state():
    """
    pytest fixture for setting default system state
    :return: None
    """
    VehicleSteps.set_gear_position(GearShifter.NEUTRAL)
    acc_pedal, brake_pedal, battery = Pin.get_object([PinsId.ACC_PEDAL, PinsId.BRAKE_PEDAL, PinsId.BATTERY])
    acc_pedal.update_object(voltage=AccPedal.STATES[AccPedal.PERCENT_0])
    brake_pedal.update_object(voltage=BrakePedal.STATES[BrakePedal.RELEASED])
    battery.update_object(voltage=Battery.STATES[Battery.READY])
