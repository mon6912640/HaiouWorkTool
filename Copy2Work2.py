from pathlib import Path
import re
from xml.etree.ElementTree import parse

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
    type_uid = ''
    str_match = ''

    def __init__(self, p_pro, p_type, p_str_match):
        self.pro = p_pro
        self.type = p_type
        self.str_match = p_str_match


code_path = 'D:/work_haiou/branch/sanguo_wechat/src'
gui_path = 'D:/work_haiou/client/sanguoUI/fabu'
xml_path = 'D:/work_haiou/client/sanguoUI/assets'
# commonBinder.ts相对于src的相对路径
commonBinder_path = 'game/Module/common/commonBinder.ts'


def run(p_gui, p_code, p_xml, p_pkg_list=None):
    path_gui = Path(p_gui)
    path_xml = Path(p_xml)
    if not path_gui.exists():
        print('指定目录不存在，程序退出')
        return

    if p_pkg_list is None or len(p_pkg_list) == 0:
        is_all = True
        print('本次将输出全部包')
    else:
        is_all = False
        print('本次将输出{0}个包'.format(len(p_pkg_list)), p_pkg_list)

    uid_map = load_xml(str(path_xml))
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
                cla_name = child.name.split('.')[0]
                url_match = re.search('static URL.+"(ui://\S+)"', string=str_gui)
                if url_match is not None:
                    key = url_match.group(1)
                    items = re.finditer('public (\w+):([\w\.]+);', str_gui, flags=re.M)
                    pro_vo_list = []
                    for m in items:
                        pro_name = m.group(1)
                        if not pro_name:  # 兼容fgui的bug，空字符串名字也给导出
                            continue
                        pro_vo = ProVo(m.group(1), m.group(2), m.group(0))
                        pro_vo_list.append(pro_vo)
                        uid_key = '{0}.{1}.{2}'.format(pkg, cla_name, pro_name)
                        # print(uid_key)
                        if uid_key in uid_map:
                            pro_vo.type_uid = uid_map[uid_key]
                    if len(pro_vo_list) > 0:
                        vo = DataVo(key, p_name=child.name, p_pkg=pkg, p_pro_list=pro_vo_list)
                        vo_map[key] = vo
    if len(vo_map) > 0:
        replace_code(p_code, vo_map)


def load_xml(p_xml):
    path_xml = Path(p_xml)
    uid_map = {}
    for dir in path_xml.iterdir():
        if not dir.is_dir():
            continue
        pkg = dir.name  # 包名
        list_file = sorted(dir.rglob('*.xml'))
        for v in list_file:
            if v.name == 'package.xml':
                continue
            cla_name = v.name.split('.')[0]  # 类名
            # print(cla_name)
            xml_vo = parse(str(v))
            name_map = {}
            for com in xml_vo.iterfind('displayList/'):
                com_name = com.get('name')
                pkg_id = com.get('pkg')
                if pkg_id is None:
                    continue
                src_id = com.get('src')
                if src_id is None:
                    continue
                if not com_name:  # 兼容fgui的bug，空字符串名字也给导出
                    continue
                # 重名处理，按照fgui的规则来
                if com_name in name_map:
                    name_map[com_name] = name_map[com_name] + 1
                    com_name = com_name + '_' + str(name_map[com_name])
                else:
                    name_map[com_name] = 1
                uid = 'ui://{0}{1}'.format(pkg_id, src_id)
                uid_key = '{0}.{1}.{2}'.format(pkg, cla_name, com_name)
                uid_map[uid_key] = uid
    return uid_map


def replace_code(p_code_path, p_vo_map):
    path_code = Path(p_code_path)
    uid_cla_map = analyze_common(p_code_path, commonBinder_path)
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
            result = ''
            for pro_vo in vo.pro_list:
                str_type = pro_vo.type
                # print(pro_vo.type_uid)
                # 分析代码中的commonBinder.ts，把属性的类替换成具体映射的类，避免手动对类定义作二次修改
                if pro_vo.type_uid and pro_vo.type_uid in uid_cla_map:
                    str_type = uid_cla_map[pro_vo.type_uid]
                result += '\t' + 'public {0}: {1};'.format(pro_vo.pro, str_type) + '\n'
            result = m.group(1) + '\n' + result + '\t' + m.group(3)
            return result.rstrip('\n')

        output_str = re.sub('(//<<<<start)(.+?)(//>>>>end)', rpl_func, str_code, flags=re.M | re.DOTALL)
        v.write_text(output_str, encoding='utf-8')
        count += 1
        print('成功修改了 {0}'.format(v.name))
    print('...本次运行共修改了{0}个文件'.format(count))


def analyze_common(p_code, p_commonBinder_path):
    path_code = Path(p_code)
    if not path_code.exists():
        return
    path_common = path_code / p_commonBinder_path
    if not path_common.exists():
        return
    str_common = path_common.read_text(encoding='utf-8')
    cla_map = {}
    uid_cla_map = {}
    find_list = re.findall('\((\w+)\.URL,[ *](\w+)\)', str_common)
    for v in find_list:
        cla_map[v[0]] = True
    # print(find_list)
    list_file = sorted(path_code.rglob('*.ts'))
    for v in list_file:
        cla_name = v.name.split('.')[0]
        if cla_name in cla_map:
            result = re.search('static URL.+"(ui://\S+)"', string=v.read_text(encoding='utf-8'))
            if result is None:
                continue
            uid = result.group(1)
            uid_cla_map[uid] = cla_name
    return uid_cla_map


run(gui_path, code_path, xml_path)
# analyze_common(code_path, commonBinder_path)
# load_xml(xml_path)
