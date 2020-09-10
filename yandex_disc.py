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
        lambda: requests.get(conf.base_url + '/resources/download', params=url_params, headers=conf.base_headers),
        HTTPStatus.OK)
    link = resp1.json()['href']
    resp2 = send_req_with_status_code_check(lambda: requests.get(link, headers=conf.base_headers), HTTPStatus.OK)
    file_name = cloud_path.split('/')[-1]
    with open(local_path + '/' + file_name, 'wb') as f:
        f.write(resp2.content)


def upload_file(local_path, cloud_path):
    """
    LOCALPATH is the path of a file to upload

    CLOUDPATH is the path with the name of a new file in your cloud
    """
    url_params = {'path': cloud_path}
    resp = send_req_with_status_code_check(
        lambda: requests.get(conf.base_url + '/resources/upload', params=url_params, headers=conf.base_headers),
        HTTPStatus.OK)
    link = resp.json()['href']
    with open(local_path, 'rb') as f:
        send_req_with_status_code_check(lambda: requests.put(link, data=f), HTTPStatus.CREATED)


def upload_zip_file(local_path, cloud_path):
    file_name = basename(local_path)
    zip_file_name = os.path.splitext(file_name)[0] + '.zip'
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as myzip:
        myzip.write(local_path, file_name)
    upload_file(zip_file_name, cloud_path)
    os.remove(zip_file_name)


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

    upload_file(zip_file_name, cloud_path)
    os.remove(zip_file_name)


def create_cloud_dir(cloud_path):
    send_req_with_status_code_check(lambda: requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                                                         params={'path': cloud_path}, headers=conf.base_headers),
                                    HTTPStatus.CREATED)


def get_dir(cloud_path):
    resp = send_req_with_status_code_check(
        lambda: requests.get('https://cloud-api.yandex.net/v1/disk/resources', params={'path': cloud_path},
                             headers=conf.base_headers), HTTPStatus.OK)
    for item in resp.json()['_embedded']['items']:
        print(item['path'])
