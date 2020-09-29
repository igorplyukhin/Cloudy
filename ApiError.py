import simplejson
import requests


class ApiError(Exception):
    def __init__(self, description):
        super()
        self.description = str(description)


def send_req_with_status_code_check(delegate):
    def wrapper(*args, **kwargs):
        if kwargs['ok_code'] is None:
            raise ValueError('ok_code cant be empty')
        resp = delegate(*args, **kwargs)
        check_status_code(resp, kwargs['ok_code'])
        return resp
    return wrapper


@send_req_with_status_code_check
def post_safely(url='', headers=None, params=None, data=None, ok_code=None):
    return requests.post(url=url, headers=headers, params=params, data=data)


@send_req_with_status_code_check
def get_safely(url='', headers=None, params=None, data=None, ok_code=None):
    return requests.get(url=url, headers=headers, params=params, data=data)


@send_req_with_status_code_check
def put_safely(url='', headers=None, params=None, data=None, ok_code=None):
    return requests.put(url=url, headers=headers, params=params, data=data)


def check_status_code(resp, ok_code):
    if resp.status_code != ok_code:
        try:
            try:
                error_description = resp.json()['description']
            except KeyError:
                error_description = resp.json()['error_summary']
        except (simplejson.errors.JSONDecodeError, KeyError):
            error_description = resp.text
        raise ApiError(error_description)
