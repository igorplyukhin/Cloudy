import unittest
import yandex_disc as yd
import dropbox as db
import random
import os

test_dir_name = f'/test_dir{random.randint(100, 1000)}'
upload_file_name = 'requirements.txt'
upload_dir_name = 'test_dir'
download_dir_name = 'test_dir'


def get_first_digit_of_status_code(status_code):
    return str(status_code)[0]


class YandexDiscTests(unittest.TestCase):
    def assert_first_digit_equals_2(self, resp):
        self.assertEqual(str(resp.status_code)[0], '2')

    def test_01_mkdir(self):
        resp = yd.mkdir(test_dir_name)
        self.assert_first_digit_equals_2(resp)

    def test_02_upload_file(self):
        resp = yd.upload_file(upload_file_name, test_dir_name)
        self.assert_first_digit_equals_2(resp)

    def test_03_download_file(self):
        resp = yd.download_file(download_dir_name, f'{test_dir_name}/{upload_file_name}')
        self.assert_first_digit_equals_2(resp)
        os.remove(f'{download_dir_name}/{upload_file_name}')

    def test_04_list(self):
        resp = yd.list_dir(test_dir_name)
        self.assert_first_digit_equals_2(resp)
        self.assertIn(upload_file_name, resp.text)

    def test_05_upload_dir(self):
        yd.upload_dir(upload_dir_name, test_dir_name)
        resp = yd.list_dir(f'{test_dir_name}/{upload_dir_name}')
        local_file_list = os.listdir(upload_dir_name)
        cloud_file_list = resp.text
        for file in local_file_list:
            self.assertIn(file, cloud_file_list)

    def test_06_rm(self):
        resp = yd.rm(test_dir_name)
        self.assert_first_digit_equals_2(resp)


class DropboxTests(unittest.TestCase):
    def assert_first_digit_equals_2(self, resp):
        self.assertEqual(str(resp.status_code)[0], '2')

    def test_01_mkdir(self):
        resp = db.mkdir(test_dir_name)
        self.assert_first_digit_equals_2(resp)

    def test_02_upload_file(self):
        resp = db.upload_file(upload_file_name, test_dir_name)
        self.assert_first_digit_equals_2(resp)

    def test_03_download_file(self):
        resp = db.download_file(download_dir_name, f'{test_dir_name}/{upload_file_name}')
        self.assert_first_digit_equals_2(resp)
        os.remove(f'{download_dir_name}/{upload_file_name}')

    def test_04_list(self):
        resp = db.list_dir(test_dir_name)
        self.assert_first_digit_equals_2(resp)
        self.assertIn(test_dir_name, resp.text)

    def test_08_rmdir(self):
        resp = db.rm(test_dir_name)
        self.assert_first_digit_equals_2(resp)


if __name__ == '__main__':
    unittest.main(failfast=True)
