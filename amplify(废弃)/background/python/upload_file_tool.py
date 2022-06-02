import logging
import os

# amplify 依赖的功能目录
project_path = '/Users/peterlee/work/Editor_iOS'
s3_command = '/Users/peterlee/editor_stickers/amplify/amplify-s3/index.js'
ds_command = '/Users/peterlee/editor_stickers/amplify/amplify-ds/index.js'

def upload_s3_file(file_path,dest_path):
    os.system("cd %s; %s upload %s %s" % (project_path, s3_command, file_path, dest_path))

def import_ds_file(model_command, file_path):
    os.system("cd %s; %s import %s %s" % (project_path, ds_command, model_command, file_path))

def export_ds_file(model_command, file_path):
    os.system("cd %s; %s export %s %s" % (project_path, ds_command, model_command, file_path))

def upload_file_s3(file_path, dest_path):
    if os.path.exists(file_path):
        upload_s3_file(file_path, dest_path)
    else:
        logging.error('no such file : %s', file_path)

def upload_file_ds(file_path, command):
    if os.path.exists(file_path):
        import_ds_file(command, file_path)
    else:
        logging.error('no such file : %s', file_path)

# local_file： full path for file source
def upload_preview_file(local_file):
    dest = 'background/previews'
    upload_file_s3(local_file,dest)


# local_file： full path for file source
def upload_download_file(local_file):
    dest = 'background/download'
    upload_file_s3(local_file, dest)

# local_file： full path for file source
def upload_tab_file(local_file):
    dest = 'background/tab/previews'
    upload_file_s3(local_file, dest)

def upload_excel_file(excel_file):
    command = 'Background'
    upload_file_ds(command, excel_file)

def export_csv_file(des_path):
    command = 'Background'
    import_ds_file(command, des_path)
