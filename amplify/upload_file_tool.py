import logging
import os

# amplify 依赖的功能目录
project_path = '/Users/peterlee/work/Editor_iOS'

def upload_file(command,file_path,dest_path):
    os.system("cd %s; %s upload %s %s" % (project_path, command, file_path, dest_path))

def import_file(command, file_path, dest_path):
    os.system("cd %s; %s import %s %s" % (project_path, command, dest_path, file_path ))

def upload_file_s3(file_path, dest_path):
    command = 'amplifys3'
    if os.path.exists(file_path):
        upload_file(command, file_path, dest_path)
    else:
        logging.error('no such file : %s', file_path)

def upload_file_ds(file_path, dest_path):
    command = 'amplifyds'
    if os.path.exists(file_path):
        import_file(command, file_path, dest_path)
    else:
        logging.error('no such file : %s', file_path)

# local_file： full path for file source
def upload_preview_file(local_file):
    dest = 'sticker/previews'
    upload_file_s3(local_file,dest)


# local_file： full path for file source
def upload_download_file(local_file):
    dest = 'sticker/download'
    upload_file_s3(local_file, dest)

# local_file： full path for file source
def upload_tab_file(local_file):
    dest = 'sticker/tab/previews'
    upload_file_s3(local_file, dest)

def upload_excel_file(excel_file):
    dest = 'Sticker'
    upload_file_ds(excel_file, dest)