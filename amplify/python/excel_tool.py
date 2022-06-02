
import logging
import pandas as pd
import json


def excel_to_json(file, sheet: int=0):
    if len(file) == 0:
        return None
    infos = pd.read_excel(file, sheet)
    json_str = infos.to_json(orient='records')
    return  json.loads(json_str)


def json_to_excel(info, file, sheet: str = None):
    if len(info) != 0 and info is not None:
        data_frame = pd.DataFrame(info, index=None)
        sheet_name = 'sheet1'
        if sheet is not  None and len(sheet) > 0:
            sheet_name = sheet
        data_frame.to_excel(file, sheet_name, index=False)
    else:
        logging.info('no content')


def updateJsonInfos(origin_infos, local_infos):
    origin_infos.sort(key=lambda x:(x['primaryId']))
    local_infos.sort(key=lambda x:(x['primaryId']))
    local_count = len(local_infos)
    index = 0
    for info in origin_infos:
        index += 1
        local_info = local_infos[index - 1]
        """检查一下无效数据，替换为同行数据"""
        id_str = local_info.get('id', None)
        if id_str is None or len(id_str) == 0:
            local_infos[index - 1] = info
            continue
        if local_count < index:
            # 新增的
            local_infos.append(info)
        else:
            # 老的数据
            # 更新特定字段 online vipState sort
            key_list = ['online', 'vipState', 'sort']
            for key in key_list:
                local_value = local_info.get(key, None)
                origin_value = info.get(key, None)
                if local_value is not None and str(local_value) != str(origin_value):
                    local_info[key] = origin_value
    return local_infos
