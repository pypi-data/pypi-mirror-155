from typing import Any, Dict, List, Optional

import logging

logger = logging.getLogger(__name__)

class ESICentroDevice:
    """[summary]"""

    __slots__ = [
        #"device_id",
        "device_type",
        "device_preset_temps",
        "online",
        #"device_name",
        "current_temperature",
        "inside_temperature",
        "program_mode",
        "dis_on_off",
        "work_mode",
        "th_work",
        "fornt_work_mode_tempara",
        "fwd",
        "event_count",
        "device_mac",
        "device_version",
        "new_version",
        "gateway_standby",
        "lock_screen",
        "password",
        "boost_duration",
        "boost_start",
        "remaining",
        "departure_time",
        "return_time",
        "device_ip_address",
        "device_sak",
        "device_sn",
        "super_device_type",
        "upgrading",
        "encryption",
        "holiday_mode",
        "holiday_record",
        "holiday_temparature",
        "command_type1",
        "command_type2",
        "auto_temp",
        "gateway_type",
        "app_online_count",
        "device_time",
        "upgrade",
        "app_request_binding_time",
    ]

    def __init__(self, device_data):

        device_data = device_data[0]
        self.device_id = device_data["device_id"]
        self.device_type = device_data["device_type"]
        self.device_preset_temps = device_data["presetsTemp"]
        self.online = device_data["online"]
        self.device_name = device_data["device_name"]
        self.current_temperature = device_data["current_temprature"]
        self.inside_temperature = device_data["inside_temparature"]
        self.program_mode = device_data["program_mode"]
        self.dis_on_off = device_data["disOnOff"]
        self.work_mode = device_data["work_mode"]
        self.th_work = device_data["th_work"]
        self.fornt_work_mode_tempara = device_data["frontWorkModeTempara"]
        self.fwd = device_data["fwD"]
        self.event_count = device_data["event_count"]
        self.device_mac = device_data["device_mac"]
        self.device_version = device_data["device_version"]
        self.new_version = device_data["new_version"]
        self.gateway_standby = device_data["gatewayStandby"]
        self.lock_screen = device_data["lockScreen"]
        self.password = device_data["password"]
        self.boost_duration = device_data["boost_duration"]
        self.boost_start = device_data["boost_start"]
        self.remaining = device_data["remaining"]
        self.departure_time = device_data["departure_time"]
        self.return_time = device_data["return_time"]
        self.device_ip_address = device_data["device_ipAddress"]
        self.device_sak = device_data["device_sak"]
        self.device_sn = device_data["device_sn"]
        self.super_device_type = device_data["superDeviceType"]
        self.upgrading = device_data["upgrading"]
        self.encryption = device_data["encryption"]
        self.holiday_mode = device_data["holidayMode"]
        self.holiday_record = device_data["holidayRecord"]
        self.holiday_temparature = device_data["holidayTemparature"]
        self.command_type1 = device_data["command_type1"]
        self.command_type2 = device_data["command_type2"]
        self.auto_temp = device_data["autoTemp"]
        self.gateway_type = device_data["gatewayType"]
        self.app_online_count = device_data["appOnlineCount"]
        self.device_time = device_data["deviceTime"]
        self.upgrade = device_data["upgrade"]
        self.app_request_binding_time = device_data["appRequestBindingTime"]

    @property
    def device_id(self):
        return self.device_id

    @property
    def device_name(self):
        return self.device_name
