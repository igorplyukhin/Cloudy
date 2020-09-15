import requests
import json
import config as conf
import os
from ApiError import send_req_with_status_code_check
from http import HTTPStatus

UPLOAD_REQUEST_LIMIT_BYTES = 1024 ** 2 * 150


def download_file(local_path, cloud_path):
    if not os.path.exists(local_path):
        raise FileNotFoundError
    headers = conf.DROPBOX_AUTH_HEADERS
    headers['Dropbox-API-Arg'] = json.dumps({'path': cloud_path})
    resp = send_req_with_status_code_check(
        lambda: requests.post(url=f'{conf.DROPBOX_CONTENT_URL}/download', headers=headers), HTTPStatus.OK)
    file_name = cloud_path.split('/')[-1]
    with open(f'{local_path}/{file_name}', 'wb') as f:
        f.write(resp.content)
    return resp


def get_dir(cloud_path):
    headers = conf.DROPBOX_AUTH_HEADERS
    headers['Content-Type'] = 'application/json'
    data = {"path": cloud_path}
    resp = send_req_with_status_code_check(
        lambda: requests.post(url=conf.DROPBOX_API_URL, headers=headers, data=json.dumps(data)), HTTPStatus.OK)

    return resp


def upload_file(local_path, cloud_path):
    file = open(local_path, 'rb')
    data = file.read(UPLOAD_REQUEST_LIMIT_BYTES)
    session_id = start_upload_session(data).json()['session_id']
    file_size = os.path.getsize(local_path)
    while file_size - file.tell() > UPLOAD_REQUEST_LIMIT_BYTES:
        offset = file.tell()#!!!
        data = file.read(UPLOAD_REQUEST_LIMIT_BYTES)
        append_to_upload_session(session_id, offset, data)

    offset = file.tell()#!!!
    data = file.read(UPLOAD_REQUEST_LIMIT_BYTES)
    resp = finish_upload_session(session_id, offset, cloud_path, data)
    file.close()
    return resp


def start_upload_session(data):
    headers = conf.DROPBOX_AUTH_HEADERS
    headers['Content-Type'] = 'application/octet-stream'
    resp = send_req_with_status_code_check(
        lambda: requests.post(url=f'{conf.DROPBOX_CONTENT_URL}/upload_session/start', headers=headers, data=data),
        HTTPStatus.OK)
    return resp


def append_to_upload_session(session_id, offset, data):
    headers = conf.DROPBOX_AUTH_HEADERS
    headers['Content-Type'] = 'application/octet-stream'
    headers['Dropbox-API-Arg'] = json.dumps({'cursor': {'session_id': session_id, 'offset': offset}})
    resp = send_req_with_status_code_check(
        lambda: requests.post(url=f'{conf.DROPBOX_CONTENT_URL}/upload_session/append_v2', headers=headers,
                              data=data), HTTPStatus.OK)
    return resp


def finish_upload_session(session_id, offset, cloud_path, data):
    headers = conf.DROPBOX_AUTH_HEADERS
    headers['Content-Type'] = 'application/octet-stream'
    headers['Dropbox-API-Arg'] = json.dumps(
        {'cursor': {'session_id': session_id, 'offset': offset}, 'commit': {'path': cloud_path}})
    resp = send_req_with_status_code_check(
        lambda: requests.post(url=f'{conf.DROPBOX_CONTENT_URL}/upload_session/finish', headers=headers, data=data),
        HTTPStatus.OK)
    return resp


if __name__ == '__main__':
    upload_file('Разгоны_.mp4', '/1234.mp4')
