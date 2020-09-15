import os
import yandex_disc
import dropbox

STORAGE = dropbox

YANDEX_TOKEN = os.getenv('YandexApiToken')

YANDEX_URL = 'https://cloud-api.yandex.net/v1/disk/resources'

YANDEX_HEADERS = {'Authorization': f'OAuth {YANDEX_TOKEN}'}

DROPBOX_TOKEN = 'R_0dEln0Nr8AAAAAAAAAAVMyyYTNvf1j91IrvAlGJwmXhA2YC1e_8-behrlifesN'

DROPBOX_CONTENT_URL = 'https://content.dropboxapi.com/2/files'

DROPBOX_API_URL = 'https://api.dropboxapi.com/2/files/list_folder'

DROPBOX_AUTH_HEADERS = {'Authorization': f'Bearer {DROPBOX_TOKEN}'}
