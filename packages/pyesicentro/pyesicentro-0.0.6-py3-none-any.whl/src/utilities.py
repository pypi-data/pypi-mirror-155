import random
from const import (
    _LOGGER,
)
import aiohttp

class Utilities:
    @classmethod
    async def make_http_request(
        cls,
        _session,
        method,
        url,
        headers=None,
        params=None,
        json_=None,
        timeout=5,
    ):

        async with _session.request(
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
                raise CentroError(cre) from cre

    @classmethod
    async def process_http_response(cls, response, response_class):
        if response["statu"]:
            response_object = response_class(response)
        else:
            print("Status is false\n")
            response_object = response_class(response)
            # print("response_object: ", response_class)

        return response_object

    async def randomMsgId() -> str:
        """randomMsgId

        Returns:
            str: a random 4 character long string, required by some requests
        """
        return "".join(random.choice("0123456789abcdef") for n in range(4))

class CentroError(Exception):
    """CentroError

    Args:
        Exception ([type]): [description]
    """

    def __init__(self, message):
        self._message = message
        super(CentroError, self).__init__(self._message)