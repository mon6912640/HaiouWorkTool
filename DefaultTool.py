from pathlib import Path
import json

"""
自动修改default.res.json文件的脚本
"""


# work_path = 'D:/work_haiou/branch/sanguo_wechat'


def run(p_work, p_clean=True):
    """
    自动修改default.res.json文件的脚本
    :param p_work: 工作目录
    :param p_clean: 是否清理不存在的资源，默认为True
    :return:
    """
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

    del_flag = False  # default删除标识
    if p_clean:
        new_list = []
        for v in obj_default['resources']:
            path_obj = path_res / v['url']
            if path_obj.exists():
                new_list.append(v)
        if len(obj_default['resources']) != len(new_list):
            obj_default['resources'] = new_list
            del_flag = True

    list_all = list_all + obj_default['resources']

    path_login = path_res / 'default.reslogin.json'
    if path_login.exists():
        str_json = path_login.read_text(encoding='utf-8')
        obj_login = json.loads(str_json)

        login_modify = False  # login修改过的标识
        if p_clean:
            new_list = []
            for v in obj_login['resources']:
                path_obj = path_res / v['url']
                if path_obj.exists():
                    new_list.append(v)
            if len(obj_login['resources']) != len(new_list):
                obj_login['resources'] = new_list
                login_modify = True

        if login_modify:
            str_result = json.dumps(obj_login, indent=4, ensure_ascii=False)
            str_result = str_result.replace('    ', '\t')  # 把四个空格转换成\t
            path_login.write_text(str_result)
            print('清理了default.reslogin.json中不存在的资源')

        list_all = list_all + obj_login['resources']

    obj_map = {}
    for v in list_all:
        url = v['url']
        if url not in obj_map:
            obj_map[url] = 1

    path_ui = path_res / 'UI'
    if not path_ui.exists():
        return
    add_flag = False  # default新增标识
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
                add_flag = True
    if add_flag or del_flag:
        str_result = json.dumps(obj_default, indent=4, ensure_ascii=False)
        str_result = str_result.replace('    ', '\t')  # 把四个空格转换成\t
        path_default.write_text(str_result)
        if add_flag and del_flag:
            print('default.res.json文件修改成功')
        elif add_flag:
            print('default.res.json文件新增了资源并成功添加')
        else:
            print('default.res.json文件清理了无用资源')
