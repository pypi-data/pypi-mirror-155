from utilities import Utilities


class ESICentroLoginResponse:
    __slots__ = [
        "_email",
        "_user_id",
        "_access_token",
    ]

    def __init__(self, response):

        self._email = response["user"]["email"]
        self._user_id = response["user"]["id"]
        self._access_token = response["user"]["token"]

    @property
    def email(self):
        return self._email

    @property
    def user_id(self):
        return self._user_id

    @property
    def access_token(self):
        return self._access_token


class RequestThermostatIDsResponse:
    __slots__ = ["_device_ids"]

    def __init__(self, response):
        self._device_ids = []
        if isinstance(response, dict):
            for (i, key) in enumerate(response):
                if isinstance(response[key], list):
                    for _devices in response[key]:
                        self._device_ids.append(_devices["device_id"])

    @property
    def device_ids(self):
        return self._device_ids


class RequestThermostatDataResponse:
    __slots__ = ["_device_data"]

    def __init__(self, response):
        self._device_data = response["devices"][0]
        Utilities._convert_temperatures(self)
        # print("self._device_data: ", self._device_data["device_id"])

    @property
    def device_data(self):
        return self._device_data


class SetThermostatTempResponse:
    __slots__ = ["_status", "_error_code", "_message", "_tcpCode"]

    def __init__(self, response):
        # print("response in class: ", response)
        if isinstance(response, dict):

            self._status = response["statu"]
            self._error_code = response["error_code"]
            self._message = response["message"]
            self._tcpCode = response["tcpCode"]

    @property
    def status(self):
        return self._status

    @property
    def message(self):
        return self._message

    @property
    def error_code(self):
        return self._error_code
