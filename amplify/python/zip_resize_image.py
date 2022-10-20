# 这是一个示例 Python 脚本。

# 按 ⌃R 执行或将其替换为您的代码。
# 按 双击 ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。
import PIL.features
from PIL import Image
import os
import zipfile
import logging
import webp
import shutil

def resize_image(file, out_file, max_width):
    """修改图片尺寸"""
    or_img = Image.open(file, 'r')
    or_width = or_img.width
    or_height = or_img.height
    resize_width = 0
    resize_height = 0
    if or_width > or_height:
        resize_width = max_width
        resize_height = or_height / or_width * resize_width
    else:
        resize_height = max_width
        resize_width = or_width / or_height * resize_height
    resiz_img = or_img.resize((int(resize_width), int(resize_height)))
    out_file_dir = os.path.dirname(out_file)
    if os.path.exists(out_file):
        return
    if os.path.exists(out_file_dir) == False:
        os.makedirs(out_file_dir)
    resiz_img.save(out_file)


def zip_image(file, zip_file):
    """压缩文件为zip"""
    if os.path.exists(os.path.abspath(zip_file)) == False:
        zipfile.ZipFile(zip_file, 'w').write(file)


def convert_webp(file, webp_file):

    file_path = str(file)
    if file_path.endswith(".gif"):
        os.system(f"ffmpeg -i {file_path} -vf scale=180:-1 -loop 0 {webp_file}")
    elif file_path.endswith(".png") or file_path.endswith(".jpg"):
        # image = Image.open(file_path)
        # image.save(webp_file, 'webp')
        os.system(f"ffmpeg -i {file_path} -vf scale=180:-1 {webp_file}")
    else:
        print('nothing do')


def convert_webp_gif(origin_home_path):
    for root, dirs, files in os.walk(origin_home_path):
        for f in files:
            file_path = os.path.join(root, f)
            if file_path.endswith("webp"):
                im = Image.open(f'{file_path}')
                path, name = os.path.split(file_path)
                im.info.pop('background', None)
                gif_name = name.replace("webp", "gif")
                git_path = os.path.join(root, "gif", gif_name)
                im.save(git_path)
                # os.system(f"ffmpeg -i {file_path} -vf scale=180:-1 {git_path}")
            else:
                logging.error(f'{file_path} does\'t match')

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':

    # textCompoundPath = "/Users/peterlee/editor_source/editor_compound_texts/thumbnail"
    # convert_webp_gif(textCompoundPath)
   imagePath = "/Users/peterlee/Documents/UI/Editor/CountriesData-ver-0.1/countries_flags_small"
   for root, dirs, files in os.walk(imagePath):
       for f in files:
           if f.endswith(".jpg"):
               parent = os.path.join(root, "thumbnail")
               if os.path.exists(parent):
                   pass
               else:
                   os.makedirs(parent)
               outpath = os.path.join(parent, f)
               path = os.path.join(root, f)
               resize_image(path, outpath, 90)

    # text_file = '/Users/peterlee/editor_source/editor_compound_texts'
    # for root, dirs, files in os.walk(text_file):
    #     for f in files:
    #         if f.endswith(".zip") == False:
    #             continue
    #         path = f.split('.')[0]
    #         new_path = os.path.join(root, path)
    #         file_path = os.path.join(root, f)
    #         thumbnail_path = os.path.join(root.replace("download", ''), 'thumbnail')
    #         is_zip = zipfile.is_zipfile(file_path)
    #         if os.path.exists(new_path):
    #             os.remove(file_path)
    #             webp_path = os.path.join(root,path, f'{path}.webp')
    #             if os.path.exists(webp_path):
    #                 shutil.move(webp_path, thumbnail_path)
    #             continue
    #         if is_zip:
    #             zipfile.ZipFile(file_path).extractall(new_path)


    # 处理gif文件修改为webp并且更改尺寸比例
    # gifFile = "/Users/peterlee/editor_source/editor_stickers/sticker_thumbnail/sticker_202208"
    # for root, dirs, files in os.walk(gifFile):
    #     for f in files:
    #         suffix = f.split(".")[-1]
    #         image_formats = ['gif', 'png', 'jpg']
    #         if suffix.lower() in image_formats:
    #             file_path = os.path.join(root, f)
    #
    #             webp_dir = os.path.join(root, 'webp')
    #             if os.path.exists(webp_dir) == False:
    #                 os.makedirs(webp_dir)
    #             file_name = "webp/" + f.replace(f".{suffix}", ".webp")
    #             webp_file = os.path.join(root, file_name)
    #             convert_webp(file_path, webp_file)


    # images = ['plants_2205_1','plants_2205_2','plants_2205_3','plants_2205_4','plants_2205_5', 'plants_2205_6','plants_2205_7']
    # parpath = '/Users/peterlee/eidtor_background/背景图片/'
    # for image in images:
    #     img_path = f'{parpath}download/plants/{image}.jpg'
    #     out_path = f'{parpath}thumbnail/plants/{image}.jpg'
    #     resize_image(img_path, out_path, 120)
        # zip_path = '/Users/peterlee/eidtor_background/背景图片/download/illustration/illustration_2205_1.zip'

    # resize_image(img_path, out_path, 120)
    # zip_image(img_path, zip_path)
# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
