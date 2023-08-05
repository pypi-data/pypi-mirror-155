import logging

import requests

logger = logging.getLogger(__name__)


def get(url, params=None, auth_key=None):
    resp = requests.get(url, params=params, headers={"auth_key": auth_key})

    if resp.status_code != 200:
        _exceptionMsg = "HTTP " + str(resp.status_code) + ((": " + resp.text) if resp.text else "")
        raise Exception(_exceptionMsg)

    return resp.json()


def post(url, params=None, auth_key=None):
    resp = requests.post(url, json=params, headers={"auth_key": auth_key})

    if resp.status_code != 200:
        _exceptionMsg = "HTTP " + str(resp.status_code) + ((": " + resp.text) if resp.text else "")
        raise Exception(_exceptionMsg)

    return resp.json()


def delete(url, params=None, auth_key=None):
    resp = requests.delete(url, params=params, headers={"auth_key": auth_key})

    if resp.status_code != 200:
        _exceptionMsg = "HTTP " + str(resp.status_code) + ((": " + resp.text) if resp.text else "")
        raise Exception(_exceptionMsg)

    return resp.json()
