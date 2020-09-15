import click
from config import STORAGE
from ApiError import ApiError


# TODO UnitTests

@click.group()
def cli():
    pass


@cli.command()
@click.option('-lp', '--local_path', default='.', help='Path to save file')
@click.argument('cloud_path')
def download_file(local_path, cloud_path):
    click.secho('Downloading...', fg='green')
    STORAGE.download_file(local_path, cloud_path)
    click.secho('Success', fg='green')


@cli.command()
@click.option('-z', '--is_zipped', is_flag=True, help='Specify if you want to compress file')
@click.argument('local_path')
@click.argument('cloud_path')
def upload_file(local_path, cloud_path, is_zipped):
    """
        LOCALPATH is the path of a file to upload

        CLOUDPATH is the path with the name of a new file in your cloud
    """
    if is_zipped:
        STORAGE.upload_zip_file(local_path, cloud_path)
    else:
        STORAGE.upload_file(local_path, cloud_path)


@cli.command()
@click.option('-z', '--is_zipped', is_flag=True, help='Specify if eou want to compress dir')
@click.argument('local_path')
@click.argument('cloud_path')
def upload_dir(local_path, cloud_path, is_zipped):
    if is_zipped:
        STORAGE.upload_zip_dir(local_path, cloud_path)
    else:
        STORAGE.upload_dir(local_path, cloud_path)


@cli.command()
@click.argument('cloud_path')
def get_dir(cloud_path):
    """
    Prints cloud folder contents

    :param cloud_path: Specify folder to show contents

    Yandex root folder = '/'; Dropbox root folder ''
    """
    resp = STORAGE.get_dir(cloud_path)
    try:
        for item in resp.json()['entries']:
            click.secho(item['path_display'])
    except KeyError:
        for item in resp.json()['_embedded']['items']:
            click.secho(item['path'])


@cli.command()
@click.argument('cloud_path')
def create_dir(cloud_path):
    print(STORAGE.create_cloud_dir(cloud_path))


if __name__ == '__main__':
    try:
        cli()
    except ApiError as e:
        click.secho(f'ApiError: {e.description}', fg='red', bold=True)
    except FileNotFoundError:
        click.secho('File or directory does not exist', fg='red', bold=True)
