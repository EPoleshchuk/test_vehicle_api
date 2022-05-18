from framework.utilities import BaseAPIModel


class Signal(BaseAPIModel):
    """
    Class with API Signal Model
    """
    SIG_ID_FIELD = "object_id"
    NAME_FIELDS = "name"
    VALUE_FIELDS = "value_field"

    _API_FIELDS_MAP = {
        "Name": NAME_FIELDS,
        "SigId": SIG_ID_FIELD,
        "Value": VALUE_FIELDS
    }

    endpoint = "signals"

    def __init__(self, object_id: str, **kwargs):
        """
        Constructor of Api Signal object (for inner using)
        :param object_id(str): Signal id
        :param kwargs(dict): dict with other api Signal object fields like name, value
        """
        super().__init__(object_id)
        self.name = kwargs.get(self.NAME_FIELDS)
        self.value = kwargs.get(self.VALUE_FIELDS)
