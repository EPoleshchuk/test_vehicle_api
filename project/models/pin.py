from framework.utilities import BaseAPIModel


class Pin(BaseAPIModel):
    """
    Class with API Pin Model
    """
    PIN_ID_FIELD = "object_id"
    NAME_FIELD = "name"
    VOLTAGE_FIELD = "voltage"

    _API_FIELDS_MAP = {
        "Name": NAME_FIELD,
        "PinId": PIN_ID_FIELD,
        "Voltage": VOLTAGE_FIELD
    }

    endpoint = "pins"
    update_endpoint = "update_pin"

    def __init__(self, object_id: str, **kwargs):
        """
        Constructor of Api Pin object (for inner using)
        :param object_id(str): Pin id
        :param kwargs(dict): dict with other api Pin object fields like name, voltage
        """
        super().__init__(object_id)
        self.voltage = kwargs.get(self.VOLTAGE_FIELD)
        self.name = kwargs.get(self.NAME_FIELD)

    def _update_fields(self, data: dict):
        """
        Method to update all fields after changes via api (for inner using)
        :param data(dict): Dict with Api object fields and new values
        :return: None
        """
        self.voltage = data.get(self.VOLTAGE_FIELD, self.voltage)
        self.name = data.get(self.NAME_FIELD, self.name)
