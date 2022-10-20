import os
import uuid
import pandas as ps
import excel_tool as ft
from server_tool import ToolType
import zip_resize_image as zrimg

class ModifyExcel:
    """excel文件操作的类"""
    def __init__(self, type_tool: ToolType):
        """初始化数据"""
        self.type_tool = type_tool
        self.preview_path = type_tool.value + '/previews/'
        self.download_path = type_tool.value + '/download/'
        self.tab_path = type_tool.value + '/tab/previews/'

    
    def copy_excel(self, source_path, dest_path):
        """复制excel文件"""
        infos = ft.excel_to_json(source_path, 0)
        ft.json_to_excel(infos, dest_path)

    
    def append_colums_to_excel(self, path):
        """直接追加 id, primaryId, downloadUrl, thumbnailUrl, upload等字段"""
        print(f"start to append colums to excel to {path}")
        infos = ft.excel_to_json(path, 0)
        index = 0
        changed = False
        for info in infos:
            index = index + 1
            file_name = info.get('filename', None)
            op_id = info.get('opId', None)
            is_upload = info.get('upload', False)
            if is_upload:
                continue
            if file_name is not None and len(file_name) != 0:
                changed = True
                id_str = info.get('id', None)
                info['upload'] = False
                if id_str is None or len(id_str) == 0:
                    info['id'] = str(uuid.uuid1())

                info['downloadUrl'] = self.download_path + file_name

                if self.type_tool == ToolType.background:
                    info['thumbnailUrl'] = self.preview_path + file_name
                else:
                    thumbnail_path = info.get('thumbnail_path', None)
                    thumbnail_name = os.path.basename(thumbnail_path)
                    if thumbnail_name is not None and len(thumbnail_name) > 0:
                        info['thumbnailUrl'] = self.preview_path + thumbnail_name
                    else:
                        info['thumbnailUrl'] = self.preview_path + op_id + '.png'

        if changed:
            ft.json_to_excel(infos, path)
        print('append colums to excel finished')

    @staticmethod
    def get_category_id(infos, category_name):
        for info in infos:
            name = info.get('name', None)
            if name == category_name and name is not None:
                return info.get('id', None)
        return None

    def setup_category_id(self, file_path, category_id_name, category_path):
        """添加category_id 到表中"""
        print(f'start setup_category_id to {file_path} category_name {category_id_name}')
        infos = ft.excel_to_json(file_path)
        category_infos = ft.excel_to_json(category_path)
        category_id_str = ''
        category_str = ''
        changed = False
        for info in infos:
            category_name = info.get(category_id_name, None)
            if category_name is not None:
                continue
            category_info = info.get('category', None)
            categogry_id = self.get_category_id(category_infos, category_info)
            if categogry_id is not None:
                category_id_str = categogry_id

            if len(category_str) == 0:
                category_str = category_info
                changed = True
            elif category_info != category_str and category_info is not None:
                category_str = category_info
                changed = True
            info[category_id_name] = category_id_str
        if changed:
            ft.json_to_excel(infos, file_path, '')
        print('setup_category_id finished')

    def modify_excel(self, source_path, dest_path):
        print(f'modify bg excel from {source_path} to {dest_path}')
        if not os.path.exists(dest_path):
            self.copy_excel(source_path, dest_path)
        else:
            source_infos = ft.excel_to_json(source_path, 0)
            dest_infos = ft.excel_to_json(dest_path, 0)
            dest_infos = ft.update_json_infos(source_infos, dest_infos)
            ft.json_to_excel(dest_infos, dest_path)
        self.append_colums_to_excel(dest_path)

    #  category
    def add_colums_to_category_excel(self, source_path, dest_path):
        infos = ft.excel_to_json(source_path, sheet=1)
        new_infos = []
        if os.path.exists(dest_path):
            new_infos = ft.excel_to_json(dest_path, 0)

        new_infos = ft.update_json_infos(infos, new_infos)
        count = len(new_infos)
        index = 0
        for info in infos:
            index += 1
            file_name = info.get('filename', None)
            op_id = info.get('opId', None)
            if op_id is None or len(op_id) == 0:
                continue

            id_str = info.get('id', None)
            if id_str is None or len(id_str) == 0:
                id_str = str(uuid.uuid1())
            info['id'] = id_str

            if index > count:
                new_infos.append(info)
            elif self.type_tool == ToolType.sticker:
                new_info = new_infos[index - 1]
                cover_url = new_info.get('coverUrl', None)
                if cover_url is None or len(cover_url) == 0:
                    cover_url = self.tab_path + file_name
                new_info['coverUrl'] = cover_url
        ft.json_to_excel(new_infos, dest_path)

    # servers
    def get_server_category_excel(self, source_path, dest_path):
        infos = ft.excel_to_json(source_path, 0)
        data_columns = {'id', 'name', 'vipState', 'online', 'sort', 'opId'}
        if self.type_tool == ToolType.sticker:
            data_columns = {'id', 'name', 'vipState', 'online', 'sort', 'opId', 'coverUrl'}
        dataframe = ps.DataFrame(columns=data_columns)
        infos_new = []
        for info in infos:
            info_new = {}
            for key in dataframe.columns:
                info_value = info.get(key, None)
                info_new[key] = info_value
            infos_new.append(info_new)
        dataframe = ps.DataFrame(infos_new, index=None)
        dataframe.to_csv(dest_path, index=False)

    def get_server_excel(self, source_path, dest_path):
        """覆盖原来的下载的文件"""
        print(f'start get_server_excel from {source_path} to {dest_path}')
        infos = ft.excel_to_json(source_path, 0)
        data_columns = {'id', 'online', 'sort', 'type', 'opId', 'thumbnailUrl', 'downloadUrl'}
        if self.type_tool == ToolType.sticker:
            data_columns = {'id', 'online', 'sort', 'type', 'opId', 'thumbnailUrl', 'downloadUrl', 'gif'}
        data_frame = ps.DataFrame(columns=data_columns)
        infos_new = []
        for info in infos:
            info_new = {}
            for key in data_frame.columns:
                if key == 'type':
                    info_value = info.get('category', None)
                    info_new[key] = info_value
                elif key == 'gif':
                    info_value = info.get('type', 'png')
                    info_new[key] = info_value == 'gif'
                else:
                    info_value = info.get(key, None)
                    info_new[key] = info_value
            infos_new.append(info_new)
        data_frame = ps.DataFrame(infos_new, index=None)
        data_frame.to_csv(dest_path, index=False)

    def zip_resize_image(self, file_path, data_path):
        """resize thumbnail image"""
        infos = ft.excel_to_json(file_path, 0)
        for info in infos:
            thumbnail = info.get('thumbnail_path', None)
            origin = info.get('origin_path', None)
            if thumbnail is not None and len(thumbnail) > 0:
                "处理压缩尺寸"
                if os.path.isfile(data_path + thumbnail):
                    print('thumbnail is exists , next.')
                    continue
                zrimg.resize_image(data_path + origin, data_path + thumbnail, 120)