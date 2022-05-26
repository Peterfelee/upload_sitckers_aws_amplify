# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
import modify_excel
import upload_file_tool
import file_tool
from concurrent.futures import ThreadPoolExecutor
import zip_resize_image as zrimg

# local path 资源文件目录
bg_data_path = '/Users/peterlee/eidtor_background/'
# amplify 生成的数据资源表
bg_data_subpath = os.getcwd().removesuffix('python') + 'data/develop/'
# bg_data_subpath = os.getcwd().removesuffix('python') + 'data/product/'
upload_file = True#False

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
        changed = True
        print(f'begin upload file at {index} line')
        if thumbnail is not  None and len(thumbnail) != 0:
            pool.submit(upload_file_tool.upload_preview_file, bg_data_path + thumbnail)
            upload_count += 1
        if origin is not None and len(origin) != 0:
            pool.submit(upload_file_tool.upload_download_file, bg_data_path + origin)
            upload_count += 1
        info['upload'] = True
        print(f'finished upload file at {index} line')
    if changed == True:
        file_tool.json_to_excel(infos, file_path)
    print(f' {upload_count} files uploaded success')

def zip_resize_image(file_path):
    infos = file_tool.excel_to_json(file_path, 0)
    for info in infos:
        thumbnail = info.get('thumbnail_path', None)
        origin = info.get('origin_path', None)
        if thumbnail is not None and len(thumbnail) > 0:
            """处理压缩"""
            zrimg.resize_image(bg_data_path + origin, bg_data_path + thumbnail, 120)

def deal_bg():
    """修改贴纸的相关数据 和 缩略图，原始图片上传"""
    original = bg_data_subpath + 'from/editor_bg_original.xlsx'
    local = bg_data_subpath + 'local/editor_bg_local.xlsx'
    server = bg_data_subpath + 'server/results_bg.csv'

    edit_excel_file(original, local)
    zip_resize_image(local)

    if upload_file:
        upload_file_from_excel(local)
    modify_excel.get_server_excel(local, server)

def deal_bg_category():
    """修改贴纸分类的相关数据 和 图片上传"""
    original = bg_data_subpath + 'from/editor_bg_original.xlsx'
    local = bg_data_subpath + 'local/editor_bg_local_category.xlsx'
    server = bg_data_subpath + 'server/results_bg_category.csv'
    modify_excel.modify_category_excel(original, local)
    modify_excel.get_server_category_excel(local, server)



def check_data():
    """仅仅处理本地数据上传s3 和 数据表格更新"""
    deal_bg_category()
    deal_bg()

def upload_data_file():
    """只处理本地的csv表格上传ds-aws"""
    server = bg_data_subpath + 'server/results_bg.csv'
    upload_file_tool.upload_file_ds(server, 'Background')
    server = bg_data_subpath + 'server/results_bg_category.csv'
    upload_file_tool.upload_file_ds(server, 'BackgroundCategory')

def pull_data():
    """只处理ds上数据拉取"""
    ds_file = bg_data_subpath + 'server/ds_result_bg.csv'
    upload_file_tool.export_ds_file('Background', ds_file)
    ds_file = bg_data_subpath + 'server/de_result_bg_category.csv'
    upload_file_tool.export_ds_file('BackgroundCategory', ds_file)

def test_pyhton():
    print('ok!!')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_pyhton()
    deal_bg()