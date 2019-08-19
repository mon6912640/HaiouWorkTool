from pathlib import Path
import json


# work_path = 'D:/work_haiou/branch/sanguo_wechat'


def run(p_work):
    path_res = Path(p_work) / 'resource'
    if not path_res.exists():
        print('指定目录不存在，程序退出')
        return

    path_default = path_res / 'default.res.json'
    if not path_default.exists():
        print('default.res.json不存在，程序退出')
        return

    list_all = []

    str_json = path_default.read_text(encoding='utf-8')
    obj_default = json.loads(str_json)
    list_all = list_all + obj_default['resources']

    path_login = path_res / 'default.reslogin.json'
    if path_login.exists():
        str_json = path_login.read_text(encoding='utf-8')
        obj_login = json.loads(str_json)
        list_all = list_all + obj_login['resources']

    obj_map = {}
    for v in list_all:
        url = v['url']
        if url not in obj_map:
            obj_map[url] = 1

    path_ui = path_res / 'UI'
    if not path_ui.exists():
        return
    modify_flag = False
    list_file = sorted(path_ui.rglob('*.*'))
    for v in list_file:
        if v.suffix == '.bin' or v.suffix == '.png' or v.suffix == '.jpg':
            url = v.relative_to(path_res).as_posix()
            if url in obj_map:
                pass
            else:
                if v.suffix == '.png' or v.suffix == '.jpg':
                    type = 'image'
                else:
                    type = 'bin'
                obj = {'url': url, 'type': type, 'name': v.name.split('.')[0]}
                obj_default['resources'].append(obj)
                modify_flag = True
    if modify_flag:
        str_result = json.dumps(obj_default, indent=4, ensure_ascii=False)
        str_result = str_result.replace('    ', '\t')  # 把四个空格转换成\t
        path_default.write_text(str_result)
        print('default.res.json文件新增了资源并成功添加')
