import config as conf
from http import HTTPStatus
import os
from ApiError import get_safely, put_safely
import common_funcs


def list_dir(cloud_path):
    return get_safely(url=conf.YANDEX_URL, params={'path': cloud_path}, headers=conf.YANDEX_HEADERS,
                      ok_code=HTTPStatus.OK)


def download_file(local_path, cloud_path):
    if not os.path.exists(local_path):
        raise FileNotFoundError
    url_params = {'path': cloud_path}
    resp1 = get_safely(url=f'{conf.YANDEX_URL}/download', params=url_params, headers=conf.YANDEX_HEADERS,
                       ok_code=HTTPStatus.OK)
    link = resp1.json()['href']
    resp2 = get_safely(url=link, headers=conf.YANDEX_HEADERS, ok_code=HTTPStatus.OK)
    file_name = cloud_path.split('/')[-1]
    with open(f'{local_path}/{file_name}', 'wb') as f:
        f.write(resp2.content)
    return resp2


def upload_file(local_path, cloud_path):
    url_params = {'path': cloud_path}
    resp = get_safely(url=f'{conf.YANDEX_URL}/upload', params=url_params, headers=conf.YANDEX_HEADERS,
                      ok_code=HTTPStatus.OK)
    link = resp.json()['href']
    with open(local_path, 'rb') as f:
        return put_safely(url=link, data=f, ok_code=HTTPStatus.CREATED)


def mkdir(cloud_path):
    return put_safely(url=conf.YANDEX_URL, params={'path': cloud_path}, headers=conf.YANDEX_HEADERS,
                      ok_code=HTTPStatus.CREATED)


def upload_dir(local_path, cloud_path):
    common_funcs.upload_dir(local_path, cloud_path, mkdir, upload_file)


def upload_zip_file(local_path, cloud_path):
    return common_funcs.upload_zip_file(local_path, cloud_path, upload_file)


def upload_zip_dir(local_path, cloud_path):
    return common_funcs.upload_zip_dir(local_path, cloud_path, upload_file)
