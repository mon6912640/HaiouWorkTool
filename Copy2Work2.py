from pathlib import Path
import re

"""
自动把生成的属性写进代码的脚本
"""


class DataVo():
    key = ''
    name = ''
    pkg = ''
    pro_list = None

    def __init__(self, p_key, p_name, p_pkg, p_pro_list):
        self.key = p_key
        self.name = p_name
        self.pkg = p_pkg
        self.pro_list = p_pro_list


class ProVo():
    pro = ''
    type = ''
    str_match = ''

    def __init__(self, p_pro, p_type, p_str_match):
        self.pro = p_pro
        self.type = p_type
        self.str_match = p_str_match


code_path = 'D:/work_haiou/branch/sanguo_wechat/src'
gui_path = 'D:/work_haiou/client/sanguoUI/fabu'


def run(p_gui, p_code, p_pkg_list=None):
    path_gui = Path(p_gui)
    if not path_gui.exists():
        print('指定目录不存在，程序退出')
        return

    if p_pkg_list is None or len(p_pkg_list) == 0:
        is_all = True
        print('本次将输出全部包')
    else:
        is_all = False
        print('本次将输出{0}个包'.format(len(p_pkg_list)), p_pkg_list)

    vo_map = {}
    for v in path_gui.iterdir():
        if v.is_dir():
            pkg = v.name
            if not is_all and pkg not in p_pkg_list:
                continue
            for child in v.iterdir():
                if not child.is_file():
                    continue
                if 'Binder.ts' in child.name:
                    continue
                str_gui = child.read_text(encoding='utf-8')
                url_match = re.search('static URL.+"(ui://\S+)"', string=str_gui)
                if url_match is not None:
                    key = url_match.group(1)
                    items = re.finditer('public (\w+):([\w\.]+);', str_gui, flags=re.M)
                    pro_vo_list = []
                    for m in items:
                        pro_vo = ProVo(m.group(1), m.group(2), m.group(0))
                        pro_vo_list.append(pro_vo)
                    if len(pro_vo_list) > 0:
                        vo = DataVo(key, p_name=child.name, p_pkg=pkg, p_pro_list=pro_vo_list)
                        vo_map[key] = vo
    if len(vo_map) > 0:
        replace_code(p_code, vo_map)


def replace_code(p_code_path, p_vo_map):
    path_code = Path(p_code_path)
    list_file = sorted(path_code.rglob('*.ts'))
    count = 0
    for v in list_file:
        str_code = v.read_text(encoding='utf-8')
        if '//<<<<start' not in str_code or '//>>>>end' not in str_code:
            continue
        result = re.search('static URL.+"(ui://\S+)"', string=str_code)
        if result is None:
            continue
        url_key = result.group(1)
        if url_key not in p_vo_map:
            continue
        vo = p_vo_map[url_key]

        def rpl_func(m):
            # TODO 需要分析代码中的commonBinder.ts，把属性的类替换成具体映射的类，避免手动对类定义作二次修改
            result = ''
            for pro_vo in vo.pro_list:
                result += '\t' + pro_vo.str_match + '\n'
            result = m.group(1) + '\n' + result + '\t' + m.group(3)
            return result.rstrip('\n')

        output_str = re.sub('(//<<<<start)(.+?)(//>>>>end)', rpl_func, str_code, flags=re.M | re.DOTALL)
        v.write_text(output_str, encoding='utf-8')
        count += 1
        print('成功修改了 {0}'.format(v.name))
    print('...本次运行共修改了{0}个文件'.format(count))
    pass


run(gui_path, code_path)
