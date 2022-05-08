import logging
import os

# amplify 依赖的功能目录
project_path = '/Users/peterlee/work/Editor_iOS'

def upload_s3_file(file_path,dest_path):
    os.system("cd %s; amplifys3 upload %s %s" % (project_path, file_path, dest_path))

def import_ds_file(model_command, file_path):
    os.system("cd %s; amplifyds import %s %s" % (project_path, model_command, file_path))

def export_ds_file(model_command, file_path):
    os.system("cd %s; amplifyds export %s %s" % (project_path, model_command, file_path))

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
    command = 'Sticker'
    upload_file_ds(command, excel_file)

def export_csv_file(des_path):
    command = 'Sticker'
    import_ds_file(command, des_path)
