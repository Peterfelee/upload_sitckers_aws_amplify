# upload_sitckers_aws_amplify
处理本地数据到excel列表，然后上传到亚马逊

1.运营只需要更新的文件为：
![img.png](img.png)
   a.如果只是修改线上数据的 上下线、vip限制、排序等，只需要通过修改
      对应的xlsx中的online， vipstate， sort等字段
   
   b. 新增资源直接下面追加对应资源的全部字段

2.修改该文件的前提是一定要确定新增的资源传到内部局域网的文件夹内部：
   1. 结构如下图：
         ![img_1.png](img_1.png)
   2. 只需要把对用资源更新后告知对应的开发来跟进处理
