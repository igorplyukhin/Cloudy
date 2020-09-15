import simplejson


class ApiError(Exception):
    def __init__(self, description):
        super()
        self.description = str(description)


def send_req_with_status_code_check(delegate, success_code):
    resp = delegate()
    if resp.status_code == success_code:
        return resp

    try:
        try:
            error_description = resp.json()['description']
        except KeyError:
            error_description = resp.json()['error_summary']
    except (simplejson.errors.JSONDecodeError, KeyError):
        error_description = resp.text
    raise ApiError(error_description)
