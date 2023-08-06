import logging

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")
_LOGGER = logging.getLogger(__name__)

# _LOGGER.setLevel(logging.DEBUG)


# CENTRO_CONFIG_FILENAME = "centro.conf"

HTTP_GET = "GET"
HTTP_POST = "POST"

CENTRO_EMAIL = "email"
CENTRO_PASSWORD = "password"

CENTRO_ENDPOINT_THERMOSTAT = "thermostat"
CENTRO_DEVICE_TYPES = "02"

CENTRO_BASE_URL = "https://esiheating.uksouth.cloudapp.azure.com/centro/"
CENTRO_LOGIN_URL = "login"
CENTRO_DEVICELIST_URL = "getDeviceList"
CENTRO_SETWORKMODE_URL = "setThermostatWorkModeNew"
CENTRO_DEVICESETTINGS_URL = "getDeviceSettingInfo"
CENTRO_SETTEMP_URL = "setThermostatTemprature"
CENTRO_MODIFYDEVICENAME_URL = "modifyDeviceName"
CENTRO_PRESETEMPS_URL = "moDevicePreTemp"
CENTRO_SETPROGBYDAY_URL = "setProgrammeByDay"
CENTRO_SETPROGITEMCOUNT_URL = "setProgrammeItemCountMode"
CENTRO_SETBOOSTMODE_URL = "setThermostatBoostModeNew"

CENTRO_WORKMODE_SCHEDULE = "0"
CENTRO_WORKMODE_5_2_SCHEDULE = "1"
CENTRO_WORKMODE_24HR_SCHEDULE = "2"
CENTRO_WORKMODE_OFF = "4"
CENTRO_WORKMODE_MANUAL = "5"

CENTRO_ACCESS_TOKEN_TIMEOUT = "1800"