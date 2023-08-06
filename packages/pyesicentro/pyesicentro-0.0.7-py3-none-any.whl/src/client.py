# from typing import Any, Dict, List, Optional

# from datetime import datetime, timedelta, timezone

from typing import Optional
from aiohttp import ClientSession, ClientResponseError

# from aiohttp.helpers import TOKEN
import logging

from const import (
    CENTRO_BASE_URL,
    CENTRO_DEVICE_TYPES,
    CENTRO_LOGIN_URL,
    CENTRO_SETWORKMODE_URL,
    HTTP_GET,
    HTTP_POST,
    CENTRO_DEVICELIST_URL,
    CENTRO_DEVICESETTINGS_URL,
    CENTRO_SETTEMP_URL,
)

from device import ESICentroDevice
from responses import ESICentroLoginResponse, SetThermostatTempResponse
from responses import RequestThermostatIDsResponse
from responses import RequestThermostatDataResponse
from utilities import Utilities

# from pyesicentro.utilities import CentroError

logger = logging.getLogger(__name__)


class ESICentroClient:
    """[summary]"""

    __slots__ = [
        "_email",
        "_password",
        "_user_id",
        "_access_token",
        "_session_details",
        "_device_ids",
    ]

    def __init__(
        self, email, password, session_details, user_id=None, access_token=None
    ):

        if session_details is not None:
            self._session_details = session_details
        else:
            self._session_details = ClientSession()

        # print("self._session_details: ", self._session_details)
        self._user_id = user_id
        self._password = password
        self._email = email
        self._access_token = access_token

    async def login(self, timeout=5):
        response = await Utilities.make_http_request(
            self._session_details,
            HTTP_POST,
            CENTRO_BASE_URL + CENTRO_LOGIN_URL,
            params={
                "email": self._email,
                "password": self._password,
            },
            timeout=timeout,
        )

        authorize_response = await Utilities.process_http_response(
            response, ESICentroLoginResponse
        )

        self._user_id = authorize_response.user_id
        self._access_token = authorize_response.access_token

        return authorize_response

    async def request_thermostat_ids(self, timeout=5):
        response = await Utilities.make_http_request(
            self._session_details,
            HTTP_GET,
            CENTRO_BASE_URL + CENTRO_DEVICELIST_URL,
            params={
                "device_type": CENTRO_DEVICE_TYPES,
                "user_id": self._user_id,
                "token": self._access_token,
            },
            timeout=timeout,
        )

        _processed_response = await Utilities.process_http_response(
            response, RequestThermostatIDsResponse
        )

        self._device_ids = _processed_response.device_ids

        return _processed_response

    async def request_thermostat_data(self, device_id, timeout=5):
        response = await Utilities.make_http_request(
            self._session_details,
            HTTP_GET,
            CENTRO_BASE_URL + CENTRO_DEVICESETTINGS_URL,
            params={
                "device_id": device_id,
                "user_id": self._user_id,
                "token": self._access_token,
            },
            timeout=timeout,
        )

        _processed_response = await Utilities.process_http_response(
            response, RequestThermostatDataResponse
        )

        # thermostat = ESICentroDevice(_processed_response.device_data)

        return _processed_response

    async def set_thermostat_temperature(
        self, device_id, current_temprature, work_mode, timeout=5
    ):
        _messageId = await Utilities.randomMsgId()
        _current_temperature = Utilities._convert_to_esi_temp(current_temprature)
        # print("current_temperature: ", _current_temperature)
        response = await Utilities.make_http_request(
            self._session_details,
            HTTP_POST,
            CENTRO_BASE_URL + CENTRO_SETWORKMODE_URL,
            params={
                "device_id": device_id,
                "current_temprature": _current_temperature,
                "user_id": self._user_id,
                "token": self._access_token,
                "work_mode": work_mode,
                "messageId": _messageId,
            },
            timeout=timeout,
        )

        _processed_response = await Utilities.process_http_response(
            response, SetThermostatTempResponse
        )

        return _processed_response
