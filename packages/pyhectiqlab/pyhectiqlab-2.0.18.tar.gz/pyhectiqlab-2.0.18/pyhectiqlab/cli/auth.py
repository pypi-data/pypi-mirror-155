import click
import getpass
import pyhectiqlab
import pyhectiqlab.ops as ops
from pyhectiqlab.auth import AuthProvider
from pyhectiqlab.mlmodels import download_mlmodel as ops_download_mlmodel
from pyhectiqlab.datasets import download_dataset as ops_download_dataset
from pyhectiqlab.apps import download_app as ops_download_app
import socket

@click.group()
def cli():
    """The official hectiqlab command line client"""
    pass

@cli.command()
def add_profile():
	auth = AuthProvider()
	username = input("Username: ")

	if auth.profile_exists(username):
		click.echo(f'A profile already exists for {username}')
		return

	password = getpass.getpass(prompt='Password: ', stream=None) 
	click.echo("Connecting...")
	success, api_key_uuid = auth.fetch_secret_api_token(username, password)

	if success:
		click.echo(f'Added profile [{username}] in {auth.tokens_path}')
		try:
			api_name = socket.gethostname()
			ops.update_secret_api_token_name(api_key_uuid, name=api_name, token=auth.secret_api_key)
			click.echo(f'Set the API-key name to {api_name}.')
		except:
			return
	else:
		click.echo('Unsuccessful login.')

@cli.command()
def version():
	click.echo(pyhectiqlab.__version__)

@cli.command()
def profiles():
	auth = AuthProvider()
	profiles = list(auth.profiles.keys())
	click.echo(profiles)

@cli.command()
@click.option('-p', '--project', prompt="Project", help='Path of the project (e.g. `hectiqai/project`)', required=True)
@click.option('-n', '--name', prompt='MLModel name', help='Name of the mlmodel', required=True)
@click.option('-v', '--version', help='Version of the mlmodel. If not specified, will download the latest release', required=False)
@click.option('-s', '--save_path', help='Save path [./]', default="./", required=False)
@click.option('-o', '--overwrite', is_flag=True)
def download_mlmodel(project, name, version, save_path, overwrite):
	dir_path = ops_download_mlmodel(mlmodel_name=name, 
						project_path=project, 
						version=version, 
						save_path=save_path, 
						overwrite=overwrite)
	if dir_path is not None:
		click.echo(f'MLModel saved in {dir_path}')

@cli.command()
@click.option('-p', '--project', prompt="Project", help='Path of the project (e.g. `hectiqai/project`)', required=True)
@click.option('-n', '--name', prompt='Dataset name', help='Name of the dataset', required=True)
@click.option('-v', '--version', help='Version of the dataset. If not specified, will download the latest release', required=False)
@click.option('-s', '--save_path', help='Save path [./]', default="./", required=True)
@click.option('-o', '--overwrite', is_flag=True)
def download_dataset(project, name, version, save_path, overwrite):
	dir_path = ops_download_dataset(dataset_name=name, 
						project_path=project, 
						version=version, 
						save_path=save_path, 
						overwrite=overwrite)
	if dir_path is not None:
		click.echo(f'Dataset saved in {dir_path}')

@cli.command()
@click.option('-p', '--project', prompt="Project", help='Path of the project (e.g. `hectiqai/project`)', required=True)
@click.option('-n', '--name', prompt='App name', help='Name of the app', required=True)
@click.option('-s', '--save_path', help='Save path [./]', default="./", required=True)
@click.option('-o', '--overwrite', is_flag=True)
@click.option('-r', '--raw', help='If set, the files are downloaded in save_path without directory', is_flag=True)
def download_app(project, name, save_path, overwrite, raw):
	dir_path = ops_download_app(app_name=name, 
						project_path=project, 
						save_path=save_path, 
						overwrite=overwrite,
						no_dir=raw)
	if dir_path is not None:
		click.echo(f'App saved in {dir_path}')
