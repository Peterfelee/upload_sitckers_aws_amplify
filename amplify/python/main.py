# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
import sys
from data_tool import DataTool
from server_tool import ToolType
import logging
import zip_resize_image

def test_yeild(params):
    for param in params:
        yield param

def helpInfo():
    checkInfo = 'check 调用check_data方法,用来处理表格数据信息和上传数据资源(s3)'
    uploadInfo = 'upload 调用upload_data_file,用来处理数据表格的上传(ds)'
    pullInfo = 'pull 调用pull_data方法,用来处理从amplify拉取数据表格到server文件夹'
    syncInfo = 'sync 调用amplfiy脚本同步数据, 默认是从dev到prod服务器, 同步的表数据是详情和分类'
    devInfo = 'dev 切换amplify的环境到dev'
    prodInfo = 'prod 切换amplify的环境到prod'
    print(f'\n{checkInfo}\n{uploadInfo}\n{pullInfo}\n{syncInfo}\n{devInfo}\n{prodInfo}')

def convert2Webp(path):
    for root, dirs, names in os.walk(path):
        print(f'root---{root}\ndirs----{dirs}\nnames-----{names}')
        for name in names:
            if len(name) > 0:
                file_path = os.path.join(root, name)
                image_type = str(name).split(".")[-1]
                webp_file = os.path.join(root,'webp')
                if os.path.exists(webp_file) == False:
                    os.makedirs(webp_file)
                webp_path = os.path.join(root,'webp',name.replace(image_type, 'webp'))
                if os.path.exists(webp_path):
                    continue
                zip_resize_image.convert_webp(str(file_path), str(webp_path))
            else:
                continue


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path = '/Users/peterlee/editor_source/editor_stickers/sticker_thumbnail/sticker_202206/neon_202206'
    # convert2Webp(path)

    agrvs = sys.argv
    command = ''
    if len(agrvs) > 1:
        command = agrvs[1]
        if '-h' in command:
            helpInfo()
            exit()
    else:
        helpInfo()
        exit()

    input_str = input('你想操作哪个分类?\na-sticker\nb-background\n')
    if input_str.capitalize() == 'A':
        type = ToolType.sticker
    elif input_str.capitalize() == 'B':
        type = ToolType.background
    elif input_str.capitalize() == 'C':
        type = ToolType.emoji
    else:
        logging.info('你没选择分类，我不知道干什么！')
        exit()
    data_tool = DataTool(type)
    input_str = input('你想要选择哪个文件夹作为资源路径：--\n')
    if input_str is not None and len(input_str) > 0 and os.path.exists(input_str):
        data_tool.data_path = input_str

    if command == 'check':
        data_tool.check_data()
    elif command == 'upload':
        data_tool.upload_data_file()
    elif command == 'pull':
        data_tool.pull_data()
    elif command == 'sync':
        models = [f'{type.name.capitalize()}', f'{type.name.capitalize()}Category']
        for model in models:
            data_tool.async_dev_pro(model)
        s3_models = [f'{type.name}/previews', f'{type.name}/tab/previews', f'{type.name}/download']
        for s3_model in s3_models:
            data_tool.sync_s3_dev_pro(s3_model)
            
    elif command == 'dev':
        data_tool.pull_to_dev()
    elif command == 'prod':
        data_tool.pull_to_pro()
    else:
        print(f'it ok! {type.name}')