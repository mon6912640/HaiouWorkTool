import argparse
import json
from pathlib import Path
from xml.etree.ElementTree import parse


class ComVo:
    id = 0
    name = ''
    pkg = ''

    def __init__(self, id, name, pkg):
        self.id = id
        self.name = name
        self.pkg = pkg


# Python3 xml相关
# https://python3-cookbook.readthedocs.io/zh_CN/latest/c06/p03_parse_simple_xml_data.html

def run(work_dir):
    path_source = Path(work_dir) / 'assets'
    print('输入的路径：{0}'.format(path_source.absolute()))

    if not path_source.exists():
        print('工作目录不存在，程序退出')
        return

    list_com = []
    list_file = sorted(path_source.rglob('package.xml'))
    for v in list_file:
        pkg = v.parent.name  # 包名
        xml_vo = parse(str(v))
        if xml_vo.getroot().tag != 'packageDescription':
            continue
        pkg_id = xml_vo.getroot().get('id')
        for com in xml_vo.iterfind('resources/'):
            # 遍历resources元素下所有元素
            uid = pkg_id + com.get('id')
            com_vo = ComVo(uid, name=com.get('name'), pkg=pkg)
            list_com.append(com_vo)

    # print(list_com)
    if len(list_com) > 0:
        list_dict = []
        for v in list_com:
            list_dict.append(v.__dict__)
        json_str = json.dumps(list_dict, indent=4, ensure_ascii=False)
        uid_file = Path(work_dir) / 'uid.txt'
        if uid_file.exists():
            uid_file.unlink()
        uid_file.write_text(json_str)
        print('共有{0}个组件资源'.format(len(list_com)))
    else:
        print('工作目录并没有导出的资源')

    print('...脚本运行结束')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='帮助信息')
    parser.add_argument('--source', type=str, default='./', help='fui工程根目录')
    args = parser.parse_args()

    run(args.source)
