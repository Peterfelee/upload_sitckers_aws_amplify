import logging
import os
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import excel_tool


class ToolType(Enum):
    sticker = "sticker"
    background = "background"


class ServerTool:
    """这是一个处理数据上报和下载的类 amplify相关"""

    def __init__(self, tool_type: ToolType, project_path, s3_command, ds_command):
        """
        初始化必须传入变量
        tool_type： 工具类的类型 python background
        project_path： 项目的根目录 amplify依赖的目录
        s3_command： 固定的s3脚本命令
        ds_command： 固定的ds脚本命令
        """
        self.tool_type = tool_type
        self.project_path = project_path
        self.s3_command = s3_command
        self.ds_command = ds_command

    def upload_s3_file(self, file_path, dest_path):
        os.system("cd %s; %s upload %s %s" % (self.project_path, self.s3_command, file_path, dest_path))

    def import_ds_file(self, model_command, file_path):
        os.system("cd %s; %s import %s %s" % (self.project_path, self.ds_command, model_command, file_path))

    def export_ds_file(self, model_command, file_path):
        os.system("cd %s; %s export %s %s" % (self.project_path, self.ds_command, model_command, file_path))

    def async_env_pro(self, model, src_env, dest_env):
        os.system("cd %s; %s sync %s %s %s" % (self.project_path, self.ds_command, model, src_env, dest_env))

    def upload_file_s3(self, file_path, dest_path):
        if os.path.exists(file_path):
            self.upload_s3_file(file_path, dest_path)
        else:
            logging.error('no such file : %s', file_path)

    def upload_file_ds(self, command, file_path):
        if os.path.exists(file_path):
            self.import_ds_file(command, file_path)
        else:
            logging.error('no such file : %s', file_path)

    # local_file： full path for file source
    def upload_preview_file(self, local_file):
        dest = self.tool_type.name + '/previews'
        self.upload_file_s3(local_file, dest)

    # local_file： full path for file source
    def upload_download_file(self, local_file):
        dest = self.tool_type.name + '/download'
        self.upload_file_s3(local_file, dest)

    # local_file： full path for file source
    def upload_tab_file(self, local_file):
        dest = self.tool_type.name + '/tab/previews'
        self.upload_file_s3(local_file, dest)

    # excel file
    def upload_excel_file(self, excel_file):
        command = str(self.tool_type.name).capitalize()
        self.upload_file_ds(command, excel_file)

    def upload_category_excel_file(self, excel_file):
        command = str(self.tool_type.name).capitalize() + 'Category'
        self.upload_file_ds(command, excel_file)

    def export_csv_file(self, des_path):
        command = str(self.tool_type.name).capitalize()
        self.export_ds_file(command, des_path)

    def export_category_csv_file(self, des_path):
        command = str(self.tool_type.name).capitalize() + 'Category'
        self.export_ds_file(command, des_path)

    # 上传文件
    def upload_file_from_excel(self, file_path, data_path):
        infos = excel_tool.excel_to_json(file_path, 0)
        changed = False
        pool = ThreadPoolExecutor(max_workers=4)
        index = 0
        upload_count = 0
        for info in infos:
            index += 1
            is_load = info.get('upload', False)
            if is_load:
                continue
            thumbnail = info.get('thumbnail_path', None)
            origin = info.get('origin_path', None)
            tab_cover = info.get('cover_path', None)
            changed = True
            print(f'begin upload file at {index} line')
            if thumbnail is not None and len(thumbnail) != 0:
                pool.submit(self.upload_preview_file, data_path + thumbnail)
                upload_count += 1
            if origin is not None and len(origin) != 0:
                pool.submit(self.upload_download_file, data_path + origin)
                upload_count += 1
            if tab_cover is not None and len(tab_cover) != 0:
                pool.submit(self.upload_tab_file, data_path + tab_cover)
                upload_count += 1
            info['upload'] = True
            print(f'finished upload file at {index} line')
        if changed:
            excel_tool.json_to_excel(infos, file_path)
        print(f' {upload_count} files uploaded success')

    def develop_to_product(self, model):
        self.async_env_pro(model, 'dev', 'prod')

    def product_to_develop(self, model):
        self.async_env_pro(model, 'prod', 'dev')
