from dcbfs.settings import *
from dcbfs.encryptor import *
import os
import click
from datetime import datetime

cli = click.Group()
def block_examination_help_text():
    '''
    Prints help text for block examination.
    '''
    print('''fields
            ------
            1-id_hash(64)
            2-timestamp(4)
            3-iv(16)
            4-md5_hash(16)
            5-content''')
    print('h for help or q for quit')


def human_readable(timestamp):
    epoch = int.from_bytes(timestamp, byteorder='big')
    hr = datetime.fromtimestamp(epoch)
    return hr.strftime('%Y-%m-%d %H:%M:%S')


@cli.command(name='examine')
def examine_block():
    '''
    Interface for examining blocks.
    '''
    try:
        block_id = input('block id to examine: ')
        if block_id == 'q':
            print("quitting")
            return
        with open(STORAGE_DIR+block_id, 'rb') as f:
            id_hash = f.read(64)
            timestamp = f.read(4)
            iv = f.read(16)
            md5_hash = f.read(16)
            content = f.read(BLOCKSIZE)
    except Exception as e:
        print("couldn't find block:", e)
        return
    block_examination_help_text()
    print('enter field number to examine:')
    while True:
        action = input('> ')
        if action == '1':
            print("id_hash:", id_hash)
        elif action == '2':
            print("timestamp:", timestamp, "=", human_readable(timestamp))
        elif action == '3':
            print("initialization vector:", iv)
        elif action == '4':
            print("md5 hash:", md5_hash)
        elif action == '5':
            print("content:", content)
        elif action == 'h' or action == 'help':
            block_examination_help_text()
        elif action == 'q':
            print("quitting")
            return
        else:
            print("invalid input")

@cli.command()
@click.option(u'--file', '-f','f', type=str, required=True)
@click.option(u'--password', '-p','password', type=str, required=True, prompt=True, hide_input=True, confirmation_prompt=True)
def upload(f, password):
    '''
    Interface for uploading files
    '''
    upload_file(f, password)

@cli.command()
def init():
    '''
    Initializes block on system
    '''
    root = os.path.expanduser("~")+'/.dcbfs/'
    strg_dir = root+'storage'
    if not os.path.exists(strg_dir):
        os.makedirs(strg_dir)
    open(root+'personal_ledger', 'a').close()

def main():
    '''Used for entry point'''
    cli()

if __name__ == '__main__':
    main()