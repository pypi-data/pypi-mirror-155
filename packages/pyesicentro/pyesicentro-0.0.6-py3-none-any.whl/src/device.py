from typing import Any, Dict, List, Optional

from const import (
    CENTRO_BASE_URL,
    HTTP_GET,
    CENTRO_DEVICELIST_URL,
    CENTRO_DEVICE_TYPES,
    CENTRO_DEVICESETTINGS_URL,
)

from datetime import datetime, timezone

from utilities import CentroError

# from pyesicentro.utilities import _request


class ESICentroDevice:
    """[summary]"""

    __slots__ = [
        "_device_id",
        "_device_type",
        "_device_preset_temps",
        "_online",
        "_device_name",
        "_current_temperature",
        "_inside_temperature",
        "_program_mode",
        "_dis_on_off",
        "_work_mode",
        "_th_work",
        "_fornt_work_mode_tempara",
        "_fwd",
        "_event_count",
        "_device_mac",
        "_device_version",
        "_new_version",
        "_gateway_standby",
        "_lock_screen",
        "_password",
        "_boost_duration",
        "_boost_start",
        "_remaining",
        "_departure_time",
        "_return_time",
        "_device_ip_address",
        "_device_sak",
        "_device_sn",
        "_super_device_type",
        "_upgrading",
        "_encryption",
        "_holiday_mode",
        "_holiday_record",
        "_holiday_temparature",
        "_command_type1",
        "_command_type2",
        "_auto_temp",
        "_gateway_type",
        "_app_online_count",
        "_device_time",
        "_upgrade",
        "_app_request_binding_time",
    ]

    def __init__(self, device_data):

        _device_data = device_data[0]
        self._device_id = _device_data["device_id"]
        self._device_type = _device_data["device_type"]
        self._device_preset_temps = _device_data["presetsTemp"]
        self._online = _device_data["online"]
        self._device_name = _device_data["device_name"]
        self._current_temperature = _device_data["current_temprature"]
        self._inside_temperature = _device_data["inside_temparature"]
        self._program_mode = _device_data["program_mode"]
        self._dis_on_off = _device_data["disOnOff"]
        self._work_mode = _device_data["work_mode"]
        self._th_work = _device_data["th_work"]
        self._fornt_work_mode_tempara = _device_data["frontWorkModeTempara"]
        self._fwd = _device_data["fwD"]
        self._event_count = _device_data["event_count"]
        self._device_mac = _device_data["device_mac"]
        self._device_version = _device_data["device_version"]
        self._new_version = _device_data["new_version"]
        self._gateway_standby = _device_data["gatewayStandby"]
        self._lock_screen = _device_data["lockScreen"]
        self._password = _device_data["password"]
        self._boost_duration = _device_data["boost_duration"]
        self._boost_start = _device_data["boost_start"]
        self._remaining = _device_data["remaining"]
        self._departure_time = _device_data["departure_time"]
        self._return_time = _device_data["return_time"]
        self._device_ip_address = _device_data["device_ipAddress"]
        self._device_sak = _device_data["device_sak"]
        self._device_sn = _device_data["device_sn"]
        self._super_device_type = _device_data["superDeviceType"]
        self._upgrading = _device_data["upgrading"]
        self._encryption = _device_data["encryption"]
        self._holiday_mode = _device_data["holidayMode"]
        self._holiday_record = _device_data["holidayRecord"]
        self._holiday_temparature = _device_data["holidayTemparature"]
        self._command_type1 = _device_data["command_type1"]
        self._command_type2 = _device_data["command_type2"]
        self._auto_temp = _device_data["autoTemp"]
        self._gateway_type = _device_data["gatewayType"]
        self._app_online_count = _device_data["appOnlineCount"]
        self._device_time = _device_data["deviceTime"]
        self._upgrade = _device_data["upgrade"]
        self._app_request_binding_time = _device_data["appRequestBindingTime"]

    @property
    def device_id(self):
        return self._device_id

    @property
    def device_name(self):
        return self._device_name
