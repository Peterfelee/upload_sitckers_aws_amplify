# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import logging
import os
import modify_excel
import  upload_file_tool
import  file_tool
from concurrent.futures import  ThreadPoolExecutor

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

# amplify 依赖的功能目录
project_path = '/Users/peterlee/work/Editor_iOS'
# local path 资源文件目录
sticker_data_path = '/Users/peterlee/editor_stickers/'
# amplify 生成的数据资源表
sticker_data_subpath = os.getcwd() + '/data/develop/'
# sticker_data_subpath = os.getcwd() + 'amplify/data/product/'


# 修改excel文件
def edit_excel_file(source, dest, category):
    modify_excel.modify_excel(source, dest, category)

# 上传文件
def upload_file_from_excel(file_path):
    infos = file_tool.excel_to_json(file_path, 0)
    changed = False
    pool = ThreadPoolExecutor(max_workers=4)
    index = 0
    for info in infos:
        index += 1
        is_load = info.get('upload', False)
        if is_load == True:
            continue
        thumbnail = info.get('thumbnail_path', None)
        origin = info.get('origin_path', None)
        tab_cover = info.get('cover_path', None)
        changed = True
        print(f'begin upload {index} file')
        if thumbnail is not  None and len(thumbnail) != 0:
            pool.submit(upload_file_tool.upload_preview_file, sticker_data_path + thumbnail)
        if origin is not None and len(origin) != 0:
            pool.submit(upload_file_tool.upload_download_file, sticker_data_path + origin)
        if tab_cover is not  None and len(tab_cover) != 0:
            pool.submit(upload_file_tool.upload_tab_file, sticker_data_path + tab_cover)
        info['upload'] = True
        print(f'finished upload {index} file')
    if changed == True:
        file_tool.json_to_excel(infos, file_path)
    print(f'all {index} files uploaded success')


def deal_sticker():
    """修改贴纸的相关数据 和 缩略图，原始图片上传"""
    original = sticker_data_subpath + 'from/editor_sticker_original.xlsx'
    local = sticker_data_subpath + 'local/editor_sticker_local.xlsx'
    server = sticker_data_subpath + 'server/results_sticker.csv'
    category_local = sticker_data_subpath + 'local/editor_sticker_local_category.xlsx'

    edit_excel_file(original, local,category_local)
    # upload_file_from_excel(local)
    modify_excel.get_server_excel(local, server)
    upload_file_tool.upload_file_ds(server, 'Sticker')

def deal_sticker_category():
    """修改贴纸分类的相关数据 和 图片上传"""
    original = sticker_data_subpath + 'from/editor_sticker_original.xlsx'
    local = sticker_data_subpath + 'local/editor_sticker_local_category.xlsx'
    server = sticker_data_subpath + 'server/results_sticker_category.csv'

    modify_excel.modify_category_excel(original, local)
    # upload_file_from_excel(local)
    modify_excel.get_server_category_excel(local, server)
    upload_file_tool.upload_file_ds(server, 'StickerCategory')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 必须先处理分类 然后根据分类生成的id来更新sticker中categryId
    deal_sticker_category()
    deal_sticker()



