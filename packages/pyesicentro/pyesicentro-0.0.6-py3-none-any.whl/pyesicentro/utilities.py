import logging
import random
import aiohttp
import asyncio

import logging

logger = logging.getLogger(__name__)

class Utilities:
    __slots__ = []

    @classmethod
    async def dictionary_to_object(
        cls,
        data,
        # property_type,
        # response_properties,
        # parent_classes=[],
        # indent=0,
        # is_top_level=False,
    ):

        if isinstance(data, dict):  # returned data is a dictionary
            for (i, key) in enumerate(data):
                print("i: ", i)
                print("key: ", key)
                if isinstance(data[key], dict):  # returned data is a dictionary
                    print("data[key]: ", data[key])
                    parent_classes = [key]
                    parent_classes.append(data[key])
                    print("parent_classes: ", parent_classes)

    @classmethod
    async def make_http_request(
        cls,
        session,
        method,
        url,
        headers=None,
        params=None,
        json_=None,
        timeout=5,
    ):

        async with session.request(
            method,
            url,
            headers=headers,
            params=params,
            json=json_,
            timeout=timeout,
        ) as response:
            try:
                response_json = await response.json(content_type="text/json")
                response.raise_for_status()

                return response_json
            except aiohttp.ClientResponseError as cre:
                raise ESICentroError(cre) from cre

    @classmethod
    async def process_http_response(cls, response, response_class):
        return response_class(response)

    async def randomMsgId() -> str:
        """randomMsgId

        Returns:
            str: a random 4 character long string, required by some requests
        """
        return "".join(random.choice("0123456789abcdef") for n in range(4))

    def convert_to_esi_temp(temp):
        return int(float(temp) * 10)

    def convert_from_esi_temp(temp):
        return float(temp) / 10

    def convert_temperatures(self):
        updates = {}
        updates.update(
            Utilities.convert_preset_temps(self.device_data["presetsTemp"])
        )
        updates.update(
            {
                "current_temprature": Utilities.convert_from_esi_temp(
                    self.device_data["current_temprature"]
                )
            }
        )
        updates.update(
            {
                "inside_temparature": Utilities.convert_from_esi_temp(
                    self.device_data["inside_temparature"]
                )
            }
        )

        self.device_data.update(updates)

    def convert_preset_temps(preset_temps):
        temps = preset_temps.split("|")

        updates = {}
        updates.update({"presetHomeTemp": Utilities.convert_from_esi_temp(temps[0])})
        updates.update(
            {"presetSleepTemp": Utilities.convert_from_esi_temp(temps[1])}
        )
        updates.update({"presetAwayTemp": Utilities.convert_from_esi_temp(temps[2])})

        return updates

class ESICentroError(Exception):
    pass

class ESICentroException(ESICentroError):
    """CentroError

    Args:
        Exception ([type]): [description]
    """

    def __init__(self, message):
        self.message = message
        super(ESICentroException, self).__init__(self.message)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

class ESICentroLoginException(ESICentroError):
    """CentroError

    Args:
        Exception ([type]): [description]
    """

    def __init__(self, message):
        self.message = message
        self.error_message = message["message"]
        super(ESICentroLoginException, self).__init__(self.error_message)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value
