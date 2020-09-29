import os
from os.path import basename
import zipfile


# test empty dir
def upload_dir(local_path, cloud_path, mkdir, upload_file):
    if not os.path.exists(local_path):
        raise FileNotFoundError

    mkdir(cloud_path)
    for filename in os.listdir(local_path):
        local_file_path = os.path.join(local_path, filename)
        cloud_file_path = os.path.join(cloud_path, filename)
        try:
            upload_file(local_file_path, cloud_file_path)
        except IsADirectoryError:
            upload_dir(local_file_path, cloud_file_path, mkdir, upload_file)


def upload_zip_dir(local_path, cloud_path, upload_file):
    zip_file_name = basename(local_path) + '.zip'
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as myzip:
        for root, dirs, files in os.walk(local_path):
            for file in files:
                myzip.write(os.path.join(root, file))

    resp = upload_file(zip_file_name, cloud_path)
    os.remove(zip_file_name)
    return resp


def upload_zip_file(local_path, cloud_path, upload_file):
    file_name = basename(local_path)
    zip_file_name = os.path.splitext(file_name)[0] + '.zip'
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as myzip:
        myzip.write(local_path, file_name)
    resp = upload_file(zip_file_name, cloud_path)
    os.remove(zip_file_name)
    return resp
