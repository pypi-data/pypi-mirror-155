from HypixelAPIWrapper.exceptions import *
from HypixelAPIWrapper.models import *
import json
import requests
from io import BytesIO
from base64 import b64decode
import python_nbt.nbt as nbt


def checkStatusCode(status_code: int, messages: list = ErrorMessages) -> None:
    if status_code == 400: raise WrongInputParams(messages[0])
    elif status_code == 403: raise WrongAPIKey(messages[1])
    elif status_code == 404: raise WrongInputParams(messages[2])
    elif status_code == 422: raise WrongInputParams(messages[3])
    elif status_code == 429: raise TooMuchRequests(messages[4])
    elif status_code == 503: raise DataIsNotPublic(messages[5])
    elif status_code != 200: raise WrongInputParams(messages[-1])

def simpleGetRequest(url: str, wrapper) -> dict:
    response: requests.Response = wrapper.get(url)
    checkStatusCode(response.status_code)
    return json.loads(response.content)

def oneParamRequest(url: str, param: str, value: str, wrapper) -> dict:
    return simpleGetRequest(f'{url}?{param}={value}', wrapper)

def threeParamsRequest(url, p1: str, p2: str, p3: str, v1: str, v2: str, v3: str, wrapper) -> dict:
    if v1 != None: return oneParamRequest(url, p1, v1, wrapper)
    elif v2 != None: return oneParamRequest(url, p2, v2, wrapper)
    elif v3 != None: return oneParamRequest(url, p3, v3, wrapper)
    else: raise WrongInputParams(ErrorMessages[0])