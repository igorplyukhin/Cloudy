#!/usr/bin/env python3
import click
from config import STORAGE
from ApiError import ApiError


# TODO UnitTests

@click.group()
def cli():
    pass


@cli.command('dfile')
@click.option('-lp', '--local_path', default='.', help='Path to save file')
@click.argument('cloud_path')
def download_file(local_path, cloud_path):
    """
        Downloads file from cloud

        CLOUDPATH is the path with the name of a new file that you want to dowload
    """
    click.secho('Downloading...', fg='green', bold=True)
    STORAGE.download_file(local_path, cloud_path)
    click.secho('Success', fg='green', bold=True)


@cli.command('ufile')
@click.option('-z', '--is_zipped', is_flag=True, help='Specify if you want to compress file')
@click.argument('local_path')
@click.argument('cloud_path')
def upload_file(local_path, cloud_path, is_zipped):
    """
        Uploads file to cloud

        LOCALPATH is the path of a file to upload './local_folder/file.txt'

        CLOUDPATH is the path with the name of a new file '/cloud_folder.txt'
    """
    click.secho('Uploading...', fg='green', bold=True)
    if is_zipped:
        STORAGE.upload_zip_file(local_path, cloud_path)
    else:
        STORAGE.upload_file(local_path, cloud_path)
    click.secho('Success', fg='green', bold=True)


@cli.command('udir')
@click.option('-z', '--is_zipped', is_flag=True, help='Specify if eou want to compress dir')
@click.argument('local_path')
@click.argument('cloud_path')
def upload_dir(local_path, cloud_path, is_zipped):
    click.secho('Uploading...', fg='green', bold=True)
    if is_zipped:
        STORAGE.upload_zip_dir(local_path, cloud_path)
    else:
        STORAGE.upload_dir(local_path, cloud_path)
    click.secho('Success', fg='green', bold=True)


@cli.command('list')
@click.argument('cloud_path')
def list_dir(cloud_path):
    """
        Prints cloud folder contents

        CLOUDPATH is folder to show contents

        Yandex root folder = '/'; Dropbox root folder ''
    """
    resp = STORAGE.list_dir(cloud_path)
    try:
        for item in resp.json()['entries']:  # Dropbox
            click.secho(item['path_display'])
    except KeyError:
        for item in resp.json()['_embedded']['items']:  # Yandex
            click.secho(item['path'])


@cli.command('mkdir')
@click.argument('cloud_path')
def mkdir(cloud_path):
    """
        Creates cloud folder

        CLOUDPATH is the path of new folder
    """
    STORAGE.mkdir(cloud_path)
    click.secho('Success', fg='green', bold=True)


@cli.command()
@click.argument('cloud_path')
def rm(cloud_path):
    """
        Delete cloud folder of file

        CLOUDPATH is the path to delete
    """
    STORAGE.rm(cloud_path)
    click.secho('Success', fg='green', bold=True)


def main():
    try:
        cli()
    except ApiError as e:
        click.secho(f'ApiError: {e.description}', fg='red', bold=True)
    except FileNotFoundError:
        click.secho('File or directory does not exist', fg='red', bold=True)


if __name__ == '__main__':
    main()
