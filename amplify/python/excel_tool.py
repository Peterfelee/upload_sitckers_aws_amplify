import json
import logging
import pandas as pd


def excel_to_json(file, sheet = 0):
    """excel的表转换为json"""
    if len(file) == 0:
        return None
    infos = pd.read_excel(file, sheet)
    json_str = infos.to_json(orient='records')
    return json.loads(json_str)


def json_to_excel(info, file, sheet = None):
    """json转换为excel文件"""
    if len(info) != 0 and info is not None:
        data_frame = pd.DataFrame(info, index=None)
        sheet_name = 'sheet1'
        if sheet is not  None and len(sheet) > 0:
            sheet_name = sheet
        data_frame.to_excel(file, sheet_name, index=False)
    else:
        logging.info('no content')


def update_json_infos(origin_infos, local_infos, update_keys = None):
    """
    根据update_keys传来的字段来更新对应的字段
    """
    if update_keys is None or update_keys.count == 0 :
        update_keys = ['online', 'vipState', 'sort']
    origin_infos.sort(key=lambda x:(x['primaryId']))
    local_infos.sort(key=lambda x:(x['primaryId']))
    local_count = len(local_infos)
    index = 0
    for info in origin_infos:
        index += 1
        if local_count < index:
            # 新增的
            local_infos.append(info)
        else:
            local_info = local_infos[index - 1]
            # 检查一下无效数据，替换为同行数据
            id_str = local_info.get('id', None)
            if id_str is None or len(id_str) == 0:
                local_infos[index - 1] = info
                continue
            # 老的数据
            # 更新特定字段 online vipState sort
            key_list = update_keys
            for key in key_list:
                local_value = local_info.get(key, None)
                origin_value = info.get(key, None)
                if local_value is not None and str(local_value) != str(origin_value):
                    local_info[key] = origin_value
                    print(f'modify:{id_str}{key}')
    return local_infos
