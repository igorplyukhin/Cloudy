import config as conf
from http import HTTPStatus
import requests
import os
from ApiError import send_req_with_status_code_check
import common_funcs


def list_dir(cloud_path):
    resp = send_req_with_status_code_check(
        lambda: requests.get(conf.YANDEX_URL, params={'path': cloud_path}, headers=conf.YANDEX_HEADERS),
        HTTPStatus.OK)
    return resp


def download_file(local_path, cloud_path):
    if not os.path.exists(local_path):
        raise FileNotFoundError
    url_params = {'path': cloud_path}
    resp1 = send_req_with_status_code_check(
        lambda: requests.get(f'{conf.YANDEX_URL}/download', params=url_params, headers=conf.YANDEX_HEADERS),
        HTTPStatus.OK)
    link = resp1.json()['href']
    resp2 = send_req_with_status_code_check(lambda: requests.get(link, headers=conf.YANDEX_HEADERS), HTTPStatus.OK)
    file_name = cloud_path.split('/')[-1]
    with open(f'{local_path}/{file_name}', 'wb') as f:
        f.write(resp2.content)
    return resp2


def upload_file(local_path, cloud_path):
    url_params = {'path': cloud_path}
    resp = send_req_with_status_code_check(
        lambda: requests.get(f'{conf.YANDEX_URL}/upload', params=url_params, headers=conf.YANDEX_HEADERS),
        HTTPStatus.OK)
    link = resp.json()['href']
    with open(local_path, 'rb') as f:
        resp = send_req_with_status_code_check(lambda: requests.put(link, data=f), HTTPStatus.CREATED)
    return resp


def create_cloud_dir(cloud_path):
    resp = send_req_with_status_code_check(
        lambda: requests.put(conf.YANDEX_URL, params={'path': cloud_path}, headers=conf.YANDEX_HEADERS),
        HTTPStatus.CREATED)
    return resp


def upload_dir(local_path, cloud_path):
    common_funcs.upload_dir(local_path, cloud_path, create_cloud_dir, upload_file)


def upload_zip_file(local_path, cloud_path):
    return common_funcs.upload_zip_file(local_path, cloud_path, upload_file)


def upload_zip_dir(local_path, cloud_path):
    return common_funcs.upload_zip_dir(local_path,cloud_path, upload_file)
