import config as conf
from http import HTTPStatus
import requests
import os
from os.path import basename
import zipfile
from ApiError import send_req_with_status_code_check


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


def upload_zip_file(local_path, cloud_path):
    file_name = basename(local_path)
    zip_file_name = os.path.splitext(file_name)[0] + '.zip'
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as myzip:
        myzip.write(local_path, file_name)
    resp = upload_file(zip_file_name, cloud_path)
    os.remove(zip_file_name)
    return resp


# test empty dir
def upload_dir(local_path, cloud_path):
    create_cloud_dir(cloud_path)
    for filename in os.listdir(local_path):
        local_file_path = os.path.join(local_path, filename)
        cloud_file_path = os.path.join(cloud_path, filename)
        upload_file(local_file_path, cloud_file_path)


def upload_zip_dir(local_path, cloud_path):
    zip_file_name = basename(local_path) + '.zip'
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as myzip:
        for root, dirs, files in os.walk(local_path):
            for file in files:
                myzip.write(os.path.join(root, file))

    resp = upload_file(zip_file_name, cloud_path)
    os.remove(zip_file_name)
    return resp


def create_cloud_dir(cloud_path):
    resp = send_req_with_status_code_check(
        lambda: requests.put(conf.YANDEX_URL, params={'path': cloud_path}, headers=conf.YANDEX_HEADERS),
        HTTPStatus.CREATED)
    return resp


def get_dir(cloud_path):
    resp = send_req_with_status_code_check(
        lambda: requests.get(conf.YANDEX_URL, params={'path': cloud_path}, headers=conf.YANDEX_HEADERS),
        HTTPStatus.OK)
    return resp
