# upload_source_aws_amplify

## 处理本地数据到excel列表，然后上传到亚马逊

1. 从运营配置的表中获取对应的字段，更新上线使用的唯一标识字段和其他技术需要的标识字段
2. 通过运营配置表from文件下的origin表格复制（做增量复制）一套新数据到local文件夹下，通常origin内的数据包含detail和category数据，这里复制到local会进行拆分 ，然后对local内数据进行追加和删除（追加id,upload等字段，删除运营自己使用的无意义字段），最后对数据进行指定的一些字段更新，同时会去检查upload字段，进行增量上传数据到amplify，到这里local表数据处理完成
3. 根据local内生成的一套中间表格，挑出数据库需要的字段进行复制（全量）到server文件内，然后调用制定脚本上传到amplify服务器
4. dev同步数据到prod： 因为dev可能存在脏数据，所以要分情况处理 a)如果只是上新数据，可以采用prod先同步到dev，然后再dev同步到prod，防止旧的线上数据因为dev而发生错误 b) 如果不只是上新数据的话，直接dev同步到prod。然后确保上线数据正常。注意： 同步数据包括两部分（数据表：amplfiyds 和 数据资源amplifys3）同步
5. auto_check_file.sh 脚本支持参数查询和参数执行

* check 调用check_data方法,用来处理表格数据信息和上传数据资源(s3)
* upload 调用upload_data_file,用来处理数据表格的上传(ds)
* pull 调用pull_data方法,用来处理从amplify拉取数据表格到server文件夹
* sync 调用amplfiy脚本同步数据, 默认是从dev到prod服务器, 同步的表数据是详情和分类
* dev 切换amplify的环境到dev
* prod 切换amplify的环境到prod

## 环境要求

1. node.js v18.0.0
2. amplify v8.1.0
3. python v3.8.9(3.0以上即可)
4. IDE - pycharm / vscode

## 运行步骤（开发）

1. 按上述配置好环境
2. 下载amplify-s3(https://github.com/milk531/amplify-s3.git) 和amplify-ds(https://github.com/milk531/amplify-ds.git)的脚本，配置脚本环境
3. 修改数据资源的路径：在Data_tool这个类的内部修改

   1. 资源文件目录 ：data_path（支持命令行外部传入绝对路径） 例如资源全路径为/User/peterlee/editor_source/editor_stickers/sticker_download/*, 那么data_path 为 /User/peterlee/editor_source/editor_stickers
   2. amplify 依赖的功能目录：project_path 就是配置了amplify服务的项目文件根目录
4. 资源文件准备：从内部服务器： 192.168.31.68 访问贴纸资源，进行下载到本地，如需要账号请直接找邓卿成
5. 请一定要将从服务器拉取的editor_xxxxx_original.xlsx文件复制到/amplify/data/develop/from
6. 将从服务器拉到的资源文件复制data_path下
7. 执行amplify文件夹下的auto_check_file.sh 查看打印日志，无误则可以开始大干一场了！！！

### 内部文件概要

* amplify：内部的文件共分为data、python 和 一个sh脚本等 三个文件（夹）
  * data：文件内部主要是处理的表格，develop和product分别是测试环境和生产环境
  * develop下三个文件

    * from：原始表格 来自资源服务器
    * local：根据原始表格进行增加，更新数据，这是一个中间表格，内部数据是衔接原始表格和上传服务器表格的全部参数
    * server：要上传到amplify服务器的数据表
  * product对应的跟上述develop一样from：原始表格 来自资源服务
* shell：主要一个文件auto_check_file.sh： 一个自动执行python内部的文件的sh脚本，这个脚本可以通过命令行参数来区分执行的动作，参数如下：
  * check： 用来更新 local内部的中间表，上传资源文件到亚马逊，并且生成server内部需要的文件
  * upload： 上传server内部生成的数据表到亚马逊
  * pull：拉取亚马逊的表格到server内部
  * dev： 切换amplify到开发环境
  * prod： 切换amplify到生产环境
  * sync: 同步amplify上的数据表格 从dev到prod
* python： 主要是更新表格，上传数据等的动作脚本
  * main.py:  主要是处理数据的更新，修改，上传等动作的入口 脚本参数都是依赖此函数内部的实现
  * data_tool.py ：内部包含一个data_tool的类，内部主要是综合处理数据表的更新复制删除以及amplify数据上传下载以及环境切换的逻辑。
  * excel_tool.py： 这个文件主要是处理excel到json的想换转换以及写入本地文件以及一个json文件根据特定字符串组更新的逻辑
  * excel_modify.py： 这个主要是调整excel内部的数据，包括字段增加和更新修改
  * server_tool.py： 这个主要是上传下载文件从s3 和 ds 等命令
  * zip_resize_image.py: 一个可以resize图片和压缩文件的类

## 运营配置须知

1. 运营只需要更新的文件为：
   1. 如果只是修改线上数据的 上下线、vip限制、排序等，只需要通过修改对应的xlsx中的online， vipstate， sort等字段
   2. 新增资源直接下面追加对应资源的全部字段
      ![img.png](img.png)
2. 修改该文件的前提是一定要确定新增的贴纸资源传到内部局域网 (192.168.31.68)的文件夹内部：
   1. 结构如下图：
      ![img_1.png](img_1.png)
   2. 只需要把对用资源更新后告知对应的开发来跟进处理
