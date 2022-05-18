from typing import Any


class Asserts:
    """
    Class with useful asserts methods
    """

    @staticmethod
    def soft_assert(received_data: dict, expected_data: dict, assert_message: str = None):
        """
        Does soft assert. Compare all values and raise AssertionError if exists
        :param received_data(dict): dict with received data like {"key1": "value1", "key2", "value2"}
        :param expected_data(dict): dict with expected data like {"key1": "value1", "key2": "value2"}
        :param assert_message(optional, [None, str]): None means use default assert message,
                                                        str - string with 3 placeholders for value, recieved_value,
                                                                                                    expected_value
        :raises: AssertionError if dicts received_data and expected_data are different
        :return: None
        """
        if not assert_message:
            assert_message = "Wrong {} value. Received={}, expected={}"

        assert_messages = []
        for key in received_data:
            if received_data[key] != expected_data[key]:
                assert_messages.append(assert_message.format(key, received_data[key], expected_data[key]))
        if assert_messages:
            raise AssertionError("\n".join(assert_messages))

    @staticmethod
    def assert_objects_equal(received_data: Any, expected_data: Any, assert_message: str = None):
        """
        Assert objects equal
        :param received_data(any): Received data
        :param expected_data(any): Expected data same type as received data
        :param assert_message(optional, [None, str]): None means use default assert message,
                                                        str - string with 2 placeholders for received_data,
                                                                                             expected_data
        :raises: AssertionError if received_data != expected_data
        :return: None
        """
        if not assert_message:
            assert_message = "Error. Received data = {}, but {} expected"

        assert received_data == expected_data, assert_message.format(received_data, expected_data)

    @staticmethod
    def assert_objects_not_equal(object1: Any, object2: Any, assert_message: str = None):
        """
        Assert objects equal
        :param object1(any): Received data
        :param object2(any): Expected data same type as object1
        :param assert_message(optional, [None, str]): None means use default assert message,
                                                        str - string with 2 placeholders for object1 value,
                                                                                             object2 value
        :raises: AssertionError if received_data == expected_data
        :return: None
        """
        if not assert_message:
            assert_message = "Error. object1 [{}] == object2 [{}]"

        assert object1 != object2, assert_message.format(object1, object2)
