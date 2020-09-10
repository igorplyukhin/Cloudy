import click
import yandex_disc as yd
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
    yd.download_file(local_path, cloud_path)
    click.secho('Success', fg='green')


@cli.command()
@click.option('-z', '--is_zipped', is_flag=True, help='Specify if you want to compress file')
@click.argument('local_path')
@click.argument('cloud_path')
def upload_file(local_path, cloud_path, is_zipped):
    if is_zipped:
        yd.upload_zip_file(local_path, cloud_path)
    else:
        yd.upload_file(local_path, cloud_path)


@cli.command()
@click.option('-z', '--is_zipped', is_flag=True, help='Specify if eou want to compress dir')
@click.argument('local_path')
@click.argument('cloud_path')
def upload_dir(local_path, cloud_path, is_zipped):
    if is_zipped:
        yd.upload_zip_dir(local_path, cloud_path)
    else:
        yd.upload_dir(local_path, cloud_path)


@cli.command()
@click.argument('cloud_path')
def get_dir(cloud_path):
    yd.get_dir(cloud_path)


if __name__ == '__main__':
    try:
        cli()
    except ApiError as e:
        click.secho(e.description, fg='red')
    except FileNotFoundError:
        click.secho('File or directory does not exist', fg='red')
