import unittest
import yandex_disc as yd
import dropbox as db
import random
import os

test_dir_name = f'/test_dir{random.randint(100, 1000)}'
upload_file_name = 'requirements.txt'
upload_dir_name = 'test_dir'


def get_first_digit_of_status_code(status_code):
    return str(status_code)[0]


class YandexDiscTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = '/'

    def assert_first_digit_equals_2(self, status_code):
        self.assertEqual(str(status_code)[0], '2')

    def test_01_mkdir(self):
        resp = yd.mkdir(test_dir_name)
        self.assert_first_digit_equals_2(resp.status_code)

    def test_02_upload_file(self):
        resp = yd.upload_file(upload_file_name, test_dir_name)
        self.assert_first_digit_equals_2(resp.status_code)

    def test_03_list(self):
        resp = yd.list_dir(test_dir_name)
        self.assert_first_digit_equals_2(resp.status_code)
        self.assertIn(upload_file_name, resp.text)

    def test_04_upload_dir(self):
        yd.upload_dir(upload_dir_name, test_dir_name)
        resp = yd.list_dir(upload_dir_name)
        local_file_list = os.listdir(upload_dir_name)
        cloud_file_list = resp.text
        for file in local_file_list:
            self.assertIn(file, cloud_file_list)

    def test_05_rm(self):
        resp = yd.rm(test_dir_name)
        self.assert_first_digit_equals_2(resp.status_code)


if __name__ == '__main__':
    unittest.main(failfast=True)
