class ApiError(Exception):
    def __init__(self, description):
        super()
        self.description = str(description)


def send_req_with_status_code_check(delegate, success_code):
    resp = delegate()
    if resp.status_code != success_code:
        raise ApiError(resp.json()['description'])
    return resp
