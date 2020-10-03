import simplejson
import requests


class ApiError(Exception):
    def __init__(self, description):
        super()
        self.description = str(description)


def send_req_with_status_code_check(delegate):
    def wrapper(*args, **kwargs):
        resp = delegate(*args, **kwargs)
        check_status_code(resp)
        return resp
    return wrapper


@send_req_with_status_code_check
def post_safely(url='', headers=None, params=None, data=None):
    return requests.post(url=url, headers=headers, params=params, data=data)


@send_req_with_status_code_check
def get_safely(url='', headers=None, params=None, data=None):
    return requests.get(url=url, headers=headers, params=params, data=data)


@send_req_with_status_code_check
def put_safely(url='', headers=None, params=None, data=None):
    return requests.put(url=url, headers=headers, params=params, data=data)


@send_req_with_status_code_check
def delete_safely(url='', headers=None, params=None, data=None):
    return requests.delete(url=url, headers=headers, params=params, data=data)


def check_status_code(resp):
    if str(resp.status_code)[0] != '2':
        try:
            try:
                error_description = resp.json()['description']
            except KeyError:
                error_description = resp.json()['error_summary']
        except (simplejson.errors.JSONDecodeError, KeyError):
            error_description = resp.text
        raise ApiError(error_description)
