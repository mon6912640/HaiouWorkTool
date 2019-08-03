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


default_work_path = 'D:/work_haiou/client/sanguo/resource/UI'
default_fabu_path = 'D:/work_haiou/client/sanguoUI/fabu'


def run(p_work_path, p_fabu_path):
    path_work = Path(p_work_path)
    path_fabu = Path(p_fabu_path)
    if not path_fabu.exists():
        print('发布目录不存在，程序退出')
        return

    path_map = {}
    list_file = sorted(path_work.rglob('*.*'))
    for v in list_file:
        if v.suffix == '.bin' or '_atlas' in v.name:
            path_map[v.name] = PathVo(v.name, v.parent)

    list_file = sorted(path_fabu.rglob('*.*'))
    for v in list_file:
        path_target = None
        if v.suffix == '.bin':
            if v.name in path_map:
                path_target = path_map[v.name].path_parent / v.name
            else:
                pkg = v.name.split('.')[0]
                path_target = path_work / pkg / v.name
                if not path_target.parent.exists():
                    path_target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(str(v), str(path_target))
        elif '_atlas' in v.name:
            if v.name in path_map:
                path_target = path_map[v.name].path_parent / v.name
            else:
                pkg = v.name.split('_')[0]
                path_target = path_work / pkg / v.name
                if not path_target.parent.exists():
                    path_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(str(v), str(path_target))

    print('成功复制bin和atlas图集到目录{0}'.format(str(path_work)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='帮助信息')
    parser.add_argument('--source', type=str, default='./fabu', help='fui工程目录')
    parser.add_argument('--to', type=str, default='./fabu2', help='输出的目录')
    args = parser.parse_args()

    run(args.source, args.to)
