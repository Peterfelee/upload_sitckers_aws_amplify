import os
from server_tool import ServerTool, ToolType
from excel_modify import ModifyExcel

#数据资源目录
sticker_data_path = '/Users/peterlee/editor_source/editor_stickers/'
bg_data_path = '/Users/peterlee/editor_source/editor_background/'
# amplify 依赖的功能目录
project_path = '/Users/peterlee/work/Editor_iOS'
s3_command = '/Users/peterlee/editor_source/amplify/amplify-s3/index.js'
ds_command = '/Users/peterlee/editor_source/amplify/amplify-ds/index.js'
# 测试环境的amplify的配置
amplify_dev = 'amplify pull --appId d36owl11o1ful4 --envName dev'
# 正式生产环境的amplify的配置 
amplify_prod = 'amplify pull --appId d36owl11o1ful4 --envName prod'


class DataTool:
    def __init__(self,tool_type: ToolType):
        """DataTool
        :param tool_type: 处理的数据类别
        # amplify 生成的数据资源表 data_path
        # local path 资源文件目录 data_subpath
        """
        self.tool_type = tool_type
        self.server_tool = ServerTool(tool_type, project_path, s3_command, ds_command)
        self.modify_excel = ModifyExcel(tool_type)
        self.upload_file = True
        self.data_subpath = os.getcwd().removesuffix('python') + 'data/develop/'
        if tool_type == ToolType.sticker:
            self.data_path = sticker_data_path
        else:
            self.data_path = bg_data_path


    def deal_data(self):
        """修改贴纸的相关数据 和 缩略图，原始图片上传"""
        tool_type_name = self.tool_type.name
        original = f'{self.data_subpath}from/editor_{tool_type_name}_original.xlsx'
        local = f'{self.data_subpath}local/editor_{tool_type_name}_local.xlsx'
        server = f'{self.data_subpath}server/results_{tool_type_name}.csv'

        self.modify_excel.modify_excel(original, local)
        # if tool_type_name == ToolType.background.name:
            # self.modify_excel.zip_resize_image(local, self.data_path)
        if self.upload_file:
            self.server_tool.upload_file_from_excel(local, self.data_path)
        self.modify_excel.get_server_excel(local, server)

    def deal_category(self):
        """修改贴纸分类的相关数据 和 图片上传"""
        tool_type_name = self.tool_type.name
        original = f'{self.data_subpath}from/editor_{tool_type_name}_original.xlsx'
        local = f'{self.data_subpath}local/editor_{tool_type_name}_local_category.xlsx'
        server = f'{self.data_subpath}server/results_{tool_type_name}_category.csv'
        self.modify_excel.add_colums_to_category_excel(original, local)
        if self.tool_type == ToolType.sticker and self.upload_file:
            self.server_tool.upload_file_from_excel(local, self.data_path)
        self.modify_excel.get_server_category_excel(local, server)

    def check_data(self):
        """仅仅处理本地数据上传s3 和 数据表格更新"""
        self.deal_category()
        self.deal_data()

    def upload_data_file(self):
        """只处理本地的csv表格上传ds-aws"""
        tool_type_name = self.tool_type.name
        server = f'{self.data_subpath}server/results_{tool_type_name}.csv'
        self.server_tool.upload_excel_file(server)
        server = f'{self.data_subpath}server/results_{tool_type_name}_category.csv'
        self.server_tool.upload_category_excel_file(server)

    def pull_data(self):
        """只处理ds上数据拉取"""
        tool_type_name = self.tool_type.name
        ds_file = f'{self.data_subpath}server/ds_result_{tool_type_name}.csv'
        self.server_tool.export_csv_file(ds_file)
        ds_file = f'{self.data_subpath}server/ds_result_{tool_type_name}_category.csv'
        self.server_tool.export_category_csv_file(ds_file)

    def async_pro_dev(self,model):
        self.server_tool.product_to_develop(model)

    def async_dev_pro(self, model):
        self.server_tool.develop_to_product(model)

    def sync_s3_dev_pro(self, model):
        self.server_tool.dev_prod_s3(model)

    def pull_to_dev(self):
        os.system("cd %s;pwd;%s" %(project_path,amplify_dev))
    
    def pull_to_pro(self):
        os.system("cd %s;pwd;%s" %(project_path,amplify_prod))