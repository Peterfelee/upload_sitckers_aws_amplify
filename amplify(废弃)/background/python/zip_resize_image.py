# 这是一个示例 Python 脚本。

# 按 ⌃R 执行或将其替换为您的代码。
# 按 双击 ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。
from PIL import Image
import os
import zipfile


def resize_image(file, out_file, max_width):
    or_img = Image.open(file,'r')
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
    out_path = os.path.dirname(out_file)
    if os.path.exists(out_file):
        return
    if os.path.exists(out_path) == False:
        os.makedirs(out_path)
    resiz_img.save(out_file)

def zip_image(file, zip_file):
    if os.path.exists(os.path.abspath(zip_file)) == False:
        zipfile.ZipFile(zip_file, 'w').write(file)




# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':

    images = ["plants_2205_1.jpg",
"plants_2205_2.jpg",
"plants_2205_3.jpg",
"plants_2205_4.jpg",
"plants_2205_5.jpg"]
    img_path = '/Users/peterlee/eidtor_background/背景图片/download/plants/'
    out_path = '/Users/peterlee/eidtor_background/背景图片/thumbnail/plants/'
    # zip_path = '/Users/peterlee/eidtor_background/背景图片/download/illustration/illustration_2205_1.zip'
    for image in images:
        resize_image(img_path + image, out_path + image, 120)
    # zip_image(img_path, zip_path)
# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
