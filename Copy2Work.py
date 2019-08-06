import argparse
import shutil
from pathlib import Path

"""
FairyGUI发布文件批量复制脚本
"""


class PathVo():
    name = ''
    path_parent: Path = None

    def __init__(self, p_name, p_path_parent):
        self.name = p_name
        self.path_parent = p_path_parent


default_fabu_path = 'D:/work_haiou/client/sanguoUI/fabu'
default_work_path = 'D:/work_haiou/client/sanguo/resource/UI'


def run(p_fabu_path, p_work_path, p_pkg_list=None):
    path_work = Path(p_work_path)
    path_fabu = Path(p_fabu_path)
    if not path_fabu.exists():
        print('发布目录不存在，程序退出')
        return

    if p_pkg_list is None or len(p_pkg_list) == 0:
        is_all = True
        print('本次将输出全部包')
    else:
        is_all = False
        print('本次将输出{0}个包'.format(len(p_pkg_list)), p_pkg_list)

    total_count = 0

    path_map = {}
    list_file = sorted(path_work.rglob('*.*'))
    for v in list_file:
        if v.suffix == '.bin' or '_atlas' in v.name:
            path_map[v.name] = PathVo(v.name, v.parent)

    list_file = sorted(path_fabu.rglob('*.*'))
    for v in list_file:
        if v.is_dir():
            continue
        path_target = None
        handle_flag = False
        if v.suffix == '.bin':
            pkg = v.name.split('.')[0]
            if not is_all and pkg not in p_pkg_list:
                continue
            if v.name in path_map:
                path_target = path_map[v.name].path_parent / v.name
            else:
                path_target = path_work / pkg / v.name
                if not path_target.parent.exists():
                    path_target.parent.mkdir(parents=True, exist_ok=True)
            handle_flag = True
        elif '_atlas' in v.name:
            pkg = v.name.split('_')[0]
            if not is_all and pkg not in p_pkg_list:
                continue
            if v.name in path_map:
                path_target = path_map[v.name].path_parent / v.name
            else:
                path_target = path_work / pkg / v.name
                if not path_target.parent.exists():
                    path_target.parent.mkdir(parents=True, exist_ok=True)
            handle_flag = True
        if handle_flag:
            shutil.copy(str(v), str(path_target))
            total_count += 1
            # print('{0}\n-->复制到{1}'.format(str(v), str(path_target)))

    print('成功复制bin和atlas图集到目录{0}，共{1}个文件'.format(str(path_work), total_count))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='帮助信息')
    parser.add_argument('--type', type=int, default=0, help='运行类型 0：参数运行 1：等待用户输入')
    parser.add_argument('--source', type=str, default='./fabu', help='fui工程的发布目录')
    parser.add_argument('--to', type=str, default='./fabu2', help='输出的目录')
    parser.add_argument('--pkg', type=str, default='', help='指定的包名称列表，用逗号分隔，默认为空则为输出所有包')
    args = parser.parse_args()

    pkg_list = []
    if args.type == 1:  # 等待用户输入
        input_pkg = input('输入你要发布的包名，多个包可用逗号分隔，不填则为输出所有包:')
        if input_pkg:
            pkg_list = input_pkg.split(',')
            print(input_pkg)
    else:  # 参数运行
        if args.pkg:
            pkg_list = args.pkg.split(',')

    run(args.source, args.to, pkg_list)
