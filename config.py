import os

token = os.getenv('YandexApiToken')

base_url = 'https://cloud-api.yandex.net/v1/disk'

base_headers = {'Authorization': f'OAuth {token}'}

cli_main_color = 'cyan'

cli_error_color = 'red'

cli_success_color = 'green'
