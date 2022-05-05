import logging
import os
import json
import datetime
import uuid

import pandas as ps
import file_tool as ft

#servers url
# server_base_url =  'https://res.editor.vidma.com/public/'
server_base_url = 'https://res.dev.editor.vidma.com/public/'
preview_path = 'sticker/previews/'
download_path = 'sticker/download/'
tab_path = 'sticker/tab/'

# 复制excel文件
def copy_excel(source_path, dest_path):
    infos = ft.excel_to_json(source_path,0)
    ft.json_to_excel(infos,dest_path)

# 直接追加 id， primaryId, downloadUrl, thumbnailUrl， upload等字段
def append_colums_to_excel(path):
    print(f'start to append_colums_to_excel to {path}')
    infos = ft.excel_to_json(path,0)
    index = 0
    changed = False
    for info in infos:
        index = index + 1
        file_name = info.get('filename', None)
        is_upload = info.get('upload', False)
        file_type = info.get('type', None)
        if is_upload == True:
            continue
        if file_name is not None and len(file_name) != 0:
            changed = True
            info['id'] = str(uuid.uuid1())
            info['primaryId'] = index
            info['downloadUrl'] = server_base_url + download_path + file_name
            info['thumbnailUrl'] = server_base_url + preview_path + file_name
            info['upload'] = False
    if changed == True:
        ft.json_to_excel(infos,path)
    print('append_colums_to_excel finished')

def get_category_id(infos, category_name):
    for info in infos:
        name = info.get('name', None)
        if name == category_name and name is not None:
            return info.get('id', None)
    return None

def setup_category_id(file_path, category_id_name, category_path):
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
        categogry_id = get_category_id(category_infos, category_info)
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
        ft.json_to_excel(infos,file_path,'')
    print('setup_category_id finished')


def get_server_excel(source_path, dest_path):
    """覆盖原来的下载的文件"""
    print(f'start get_server_excel from {source_path} to {dest_path}')
    infos = ft.excel_to_json(source_path,0)
    dataFrame = ps.DataFrame(columns={'id','thumbnailUrl','downloadUrl','online',
                                      'sort','type','stickercategoryID',
                                      'opId','primaryId'})
    infos_new = []
    for info in infos:
        info_new = {}
        for key in dataFrame.columns:
            info_value = info.get(key, None)
            info_new[key] = info_value
        infos_new.append(info_new)
    dataFrame = ps.DataFrame(infos_new, index=None)
    dataFrame.to_csv(dest_path, index=False)

def modify_excel(source_path, dest_path, category_path):
    print(f'modify excel from {source_path} to {dest_path}')
    if os.path.exists(dest_path) == False:
        copy_excel(source_path, dest_path)
    else:
        source_infos = ft.excel_to_json(source_path, 0)
        dest_infos = ft.excel_to_json(dest_path, 0)
        dest_infos = ft.updateJsonInfos(source_infos, dest_infos)
        ft.json_to_excel(dest_infos, dest_path)
    append_colums_to_excel(dest_path)
    setup_category_id(dest_path, 'stickercategoryID', category_path)

#  category
def add_colums_to_category_excel(source_path, dest_path):
    infos = ft.excel_to_json(source_path, sheet=1)
    new_infos = []
    if os.path.exists(dest_path):
        new_infos = ft.excel_to_json(dest_path, 0)
    count = len(new_infos)
    for info in infos:
        new_info = info
        file_name = info.get('filename', None)
        if file_name is  None or len(file_name) == 0:
            continue
        new_info['coverUrl'] = info.get('coverUrl', server_base_url + tab_path + file_name)
        new_info['id'] = info.get('id', str(uuid.uuid1()))
        if count == 0:
            new_infos.append(new_info)
            continue
        count -= 1
    ft.json_to_excel(new_infos, dest_path)

def get_server_category_excel(source_path, dest_path):
    infos = ft.excel_to_json(source_path, 0)
    dataFrame = ps.DataFrame(columns={'id',	'coverUrl',	'name',	'vipState','online','sort','opId'})
    infos_new = []
    for info in infos:
        info_new = {}
        for key in dataFrame.columns:
            info_value = info.get(key, None)
            info_new[key] = info_value
        infos_new.append(info_new)
    dataFrame = ps.DataFrame(infos_new, index=None)
    dataFrame.to_csv(dest_path, index=False)

def modify_category_excel(source_path, dest_path):
    """修改sticker_category文件"""
    add_colums_to_category_excel(source_path, dest_path)







if  __name__ == '__main__':
    test_path = '/Users/peterlee/editor_stickers/amplify/data/from/editor_sticker_original.xlsx'
    dest_path = '/Users/peterlee/editor_stickers/amplify/data/local/editor_sticker_local_category.xlsx'
    server_path = '/Users/peterlee/editor_stickers/amplify/data/server/results_sticker_category.csv'
    modify_category_excel(test_path, dest_path)
    get_server_category_excel(dest_path, server_path)