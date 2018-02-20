from .settings import *
from .encryptor import *
from .util import human_readable, _explore, _examine_block, _init
import os
import click
import pprint

cli = click.Group()

@cli.command(name='examine')
@click.option(u'--file', '-f','f', type=str, required=True, prompt=True)
def examine_block(f):
	'''
	Interface for examining blocks.
	'''
	_examine_block(f)

@cli.command()
@click.option(u'--file', '-f','f', type=str, required=True)
@click.option(u'--password', '-p','password', type=str, required=True, prompt=True, hide_input=True, confirmation_prompt=True)
def upload(f, password):
	'''
	Interface for uploading files
	'''
	upload_file(f, password)

@cli.command()
@click.option(u'--file', '-f','f', type=str, required=True)
def delete(f, password):
	'''
	Interface for uploading files
	'''
	delete_file(f)

@cli.command()
def explore():
	'''
	Interface for uploading files
	'''
	_explore()

@cli.command()
def init():
	_init()

def main():
	'''Used for entry point'''
	cli()

if __name__ == '__main__':
	main()
