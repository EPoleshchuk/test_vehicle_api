from project.consts import PinsId, GearShifter, AccPedal
from project.models import Pin
from project.steps import VehicleSteps, CommonSteps


class TestE2E:
    def test_drive_reverse_park(self):
        VehicleSteps.switch_gear_with_brake_pedal(GearShifter.DRIVE)
        Pin.get_object(PinsId.ACC_PEDAL).update_object(voltage=AccPedal.STATES[AccPedal.PERCENT_50])
        CommonSteps.assert_acc_pedal_and_req_torque(AccPedal.PERCENT_50)
        Pin.get_object(PinsId.ACC_PEDAL).update_object(voltage=AccPedal.STATES[AccPedal.PERCENT_0])
        CommonSteps.assert_acc_pedal_and_req_torque(AccPedal.PERCENT_0)
        VehicleSteps.switch_gear_with_brake_pedal(GearShifter.REVERSE)
        Pin.get_object(PinsId.ACC_PEDAL).update_object(voltage=AccPedal.STATES[AccPedal.PERCENT_50])
        CommonSteps.assert_acc_pedal_and_req_torque(AccPedal.PERCENT_50)
        Pin.get_object(PinsId.ACC_PEDAL).update_object(voltage=AccPedal.STATES[AccPedal.PERCENT_0])
        CommonSteps.assert_acc_pedal_and_req_torque(AccPedal.PERCENT_0)
        VehicleSteps.switch_gear_with_brake_pedal(GearShifter.PARK)
