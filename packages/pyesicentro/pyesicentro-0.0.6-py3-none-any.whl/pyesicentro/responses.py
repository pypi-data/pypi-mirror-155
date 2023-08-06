from .utilities import Utilities, ESICentroLoginException

import logging

logger = logging.getLogger(__name__)

class ESICentroLoginResponse:
    __slots__ = [
        "_email",
        "_user_id",
        "_access_token",
    ]

    def __init__(self, response):
        if response["statu"]:
            self.email = response["user"]["email"]
            self.user_id = response["user"]["id"]
            self.access_token = response["user"]["token"]

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value


class RequestThermostatIDsResponse:
    __slots__ = ["_device_ids"]

    def __init__(self, response):
        self.device_ids = []
        if isinstance(response, dict):
            for (i, key) in enumerate(response):
                if isinstance(response[key], list):
                    for devices in response[key]:
                        self.device_ids.append(devices["device_id"])

    @property
    def device_ids(self):
        return self._device_ids

    @device_ids.setter
    def device_ids(self, value):
        self._device_ids = value


class RequestThermostatDataResponse:
    __slots__ = ["_device_data"]

    def __init__(self, response):
        self.device_data = response["devices"][0]
        Utilities.convert_temperatures(self)

    @property
    def device_data(self):
        return self._device_data

    @device_data.setter
    def device_data(self, value):
        self._device_data = value


class SetThermostatTempResponse:
    __slots__ = ["_status", "_error_code", "_message", "_tcpCode"]

    def __init__(self, response):
        if isinstance(response, dict):

            self.status = response["statu"]
            self.error_code = response["error_code"]
            self.message = response["message"]
            self.tcpCode = response["tcpCode"]

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def error_code(self):
        return self._error_code

    @error_code.setter
    def error_code(self, value):
        self._error_code = value

    @property
    def tcpCode(self):
        return self._tcpCode

    @tcpCode.setter
    def tcpCode(self, value):
        self._tcpCode = value
