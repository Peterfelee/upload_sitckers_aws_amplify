# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
import modify_excel
import upload_file_tool
import file_tool
from concurrent.futures import ThreadPoolExecutor

# local path 资源文件目录
sticker_data_path = '/Users/peterlee/editor_stickers/'
# amplify 生成的数据资源表
sticker_data_subpath = os.getcwd() + '/data/develop/'
# sticker_data_subpath = os.getcwd() + '/data/product/'
upload_file = False

def edit_excel_file(source, dest):
    """修改excel文件"""
    modify_excel.modify_excel(source, dest)

# 上传文件
def upload_file_from_excel(file_path):
    infos = file_tool.excel_to_json(file_path, 0)
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
        if thumbnail is not  None and len(thumbnail) != 0:
            pool.submit(upload_file_tool.upload_preview_file, sticker_data_path + thumbnail)
            upload_count += 1
        if origin is not None and len(origin) != 0:
            pool.submit(upload_file_tool.upload_download_file, sticker_data_path + origin)
            upload_count += 1
        if tab_cover is not None and len(tab_cover) != 0:
            pool.submit(upload_file_tool.upload_tab_file, sticker_data_path + tab_cover)
            upload_count += 1
        info['upload'] = True
        print(f'finished upload file at {index} line')
    if changed == True:
        file_tool.json_to_excel(infos, file_path)
    print(f' {upload_count} files uploaded success')


def deal_sticker():
    """修改贴纸的相关数据 和 缩略图，原始图片上传"""
    original = sticker_data_subpath + 'from/editor_sticker_original.xlsx'
    local = sticker_data_subpath + 'local/editor_sticker_local.xlsx'
    server = sticker_data_subpath + 'server/results_sticker.csv'

    edit_excel_file(original, local)
    if upload_file:
        upload_file_from_excel(local)
    modify_excel.get_server_excel(local, server)

def deal_sticker_category():
    """修改贴纸分类的相关数据 和 图片上传"""
    original = sticker_data_subpath + 'from/editor_sticker_original.xlsx'
    local = sticker_data_subpath + 'local/editor_sticker_local_category.xlsx'
    server = sticker_data_subpath + 'server/results_sticker_category.csv'

    modify_excel.modify_category_excel(original, local)
    if upload_file:
        upload_file_from_excel(local)
    modify_excel.get_server_category_excel(local, server)



def check_data():
    """仅仅处理本地数据上传s3 和 数据表格更新"""
    # deal_sticker_category()
    deal_sticker()

def upload_data_file():
    """只处理本地的csv表格上传ds-aws"""
    server = sticker_data_subpath + 'server/results_sticker.csv'
    upload_file_tool.upload_file_ds(server, 'Sticker')
    # server = sticker_data_subpath + 'server/results_sticker_category.csv'
    # upload_file_tool.upload_file_ds(server, 'StickerCategory')

def pull_data():
    """只处理ds上数据拉取"""
    ds_file = sticker_data_subpath + 'server/ds_result_sticker.csv'
    upload_file_tool.export_ds_file('Sticker', ds_file)
    ds_file = sticker_data_subpath + 'server/de_result_sticker_category.csv'
    upload_file_tool.export_ds_file('StickerCategory', ds_file)

def test_pyhton():
    print('ok!!')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_pyhton()