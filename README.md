# upload_source_aws_amplify
    处理本地数据到excel列表，然后上传到亚马逊

## 环境要求(请务必注意)
    1.node.js v14.19.1 (稳定版本)
    2.amplify v8.0.1
    3.python v3.8.9(3.0以上即可)

## 运行步骤（开发）
        1.按上述配置好环境
        2.下载amplify-s3 和amplify-ds的脚本，配置脚本环境 详细参考：http://www.baidu.com
        3.修改内部的路径：
        A.local path 资源文件目录：sticker_data_path
        B.amplify 依赖的功能目录：project_path
        4.资源文件准备：从内部服务器： 192.168.31.68 访问贴纸资源，进行下载到本地，如需要账号请直接找邓卿成
        请一定要将从服务器拉取的editor_sticker_original.xlsx文件复制到/amplify/data/develop/from 和 /amplify/data/product/from
        5.将上述的sticker_data_path从服务器拉到的资源文件本地根目录
        6.shell文件夹下的auto_check_file.sh 查看打印日志，无误则可以开始大干一场了！！！
        
### 内部文件概要
        amplify：内部的文件共分为data、shell、python 三个文件
        data：文件内部主要是处理的表格，develop和product分别是测试环境和生产环境
                develop下三个文件 from：原始表格 来自资源服务器
                                local：根据原始表格进行增加，更新数据，这是一个中间表格，内部数据是衔接原始表格和上传服务器表格的全部参数
                                server：要上传到amplify服务器的数据表
                product对应的跟上述develop一样
        shell：主要一个文件auto_check_file.sh： 一个自动执行python内部的文件的sh脚本，这个脚本可以通过命令行参数来区分执行的动作
                参数：
                check： 用来更新 local内部的中间表，上传资源文件到亚马逊，并且生成server内部需要的文件
                upload： 上传server内部生成的数据表到亚马逊
                pull：拉取亚马逊的表格到server内部
        python： 主要是更新表格，上传数据等的动作脚本
                check_data.py,pull_data.py,upload_data.py 这三个是简单的用来执行main内部函数的文件，shell命令的参数支持就是这三个文件来完成。
                file_tool.py： 这个文件主要是处理excel到json的想换转换以及写入本地文件
                modify_excel.py： 这个主要是调整excel内部的数据，包括数据自段增加和更新修改
                upload_file_tool.py： 这个主要是上传下载文件从s3 和 ds 等命令
                main.py： 这个主要入口的地方，各个动作都是从这里开始，具体请看内部的注释


## 运营配置须知
    1.运营只需要更新的文件为：
        1.如果只是修改线上数据的 上下线、vip限制、排序等，只需要通过修改对应的xlsx中的online， vipstate， sort等字段
        2.新增资源直接下面追加对应资源的全部字段
![img.png](img.png)
       

    2.修改该文件的前提是一定要确定新增的贴纸资源传到内部局域网 (192.168.31.68)的文件夹内部：
        1.结构如下图：
![img_1.png](img_1.png)
        2. 只需要把对用资源更新后告知对应的开发来跟进处理
