import config as conf
import requests
import os


class YandexAPIError(Exception):
    def __init__(self, description):
        super()
        self.description = str(description)


def download_file(local_path, cloud_path):
    url_params = {'path': cloud_path}
    resp1 = send_req_with_status_code_check(
        lambda: requests.get(conf.base_url + '/resources/download', params=url_params, headers=conf.base_headers), 200)
    link = resp1.json()['href']
    resp2 = send_req_with_status_code_check(lambda: requests.get(link, headers=conf.base_headers), 200)
    file_name = cloud_path.split('/')[-1]
    with open(local_path + '/' + file_name, 'wb') as f:
        f.write(resp2.content)


def upload_file(local_path, cloud_path):
    """
    LOCALPATH is the path of a file to upload

    CLOUDPATH is the path with the name of a new file in your cloud
    """
    with open(local_path, 'rb') as f:
        url_params = {'path': cloud_path}
        resp = send_req_with_status_code_check(
            lambda: requests.get(conf.base_url + '/resources/upload', params=url_params, headers=conf.base_headers),
            200)
        link = resp.json()['href']
        send_req_with_status_code_check(lambda: requests.put(link, data=f), 201)


def upload_dir(local_path, cloud_path):
    create_cloud_dir(cloud_path)
    for filename in os.listdir(local_path):
        local_file_path = os.path.join(local_path, filename)
        cloud_file_path = os.path.join(cloud_path, filename)
        upload_file(local_file_path, cloud_file_path)


def create_cloud_dir(cloud_path):
    send_req_with_status_code_check(lambda: requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                                                         params={'path': cloud_path}, headers=conf.base_headers), 201)


def get_dir(cloud_path):
    resp = send_req_with_status_code_check(
        lambda: requests.get('https://cloud-api.yandex.net/v1/disk/resources', params={'path': cloud_path},
                             headers=conf.base_headers), 200)
    for item in resp.json()['_embedded']['items']:
        print(item['path'])


def send_req_with_status_code_check(delegate, success_code):
    resp = delegate()
    if resp.status_code != success_code:
        raise YandexAPIError(resp.json()['description'])
    return resp
