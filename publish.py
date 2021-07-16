import argparse
import sys
import json
from pathlib import Path

import Copy2Work
import Copy2Work2
import FGUICodeTool
import DefaultTool

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='帮助信息')
    parser.add_argument('--type', type=int, default=0, help='运行类型 0：参数运行 1：等待用户输入')
    parser.add_argument('--pkg', type=str, default='', help='指定的包名称列表，用逗号分隔，默认为空则为输出所有包')

    parser.add_argument('--code', type=str, default='', help='代码工程目录')
    parser.add_argument('--fgui', type=str, default='./src', help='fgui工程目录')
    parser.add_argument('--preload', type=str, default='', help='添加进预加载的包名')

    args = parser.parse_args()

    if not args.fgui:
        print('请指定fgui的工程目录')
        sys.exit()

    if not args.code:
        print('请指定代码工程目录')
        sys.exit()

    path_code = Path(args.code)
    if not path_code.exists():
        print('代码工程目录不存在')
        sys.exit()

    file_egret = path_code / 'egretProperties.json'
    if not file_egret.exists():
        print('指定的代码工程目录非Egret工程')
        sys.exit()

    path_fgui = Path(args.fgui)
    if not path_fgui.exists():
        print('fgui工程目录不存在')
        sys.exit()

    f_list = sorted(path_fgui.glob('*.fairy'))
    if len(f_list) < 1:
        print('指定的fgui工程目录错误')
        sys.exit()

    # 读取fgui工程的配置，读取图集发布目录和代码发布目录
    publish_json = (path_fgui / 'settings' / 'Publish.json').read_text(encoding='utf-8')
    obj_publish = json.loads(publish_json)
    path_bin_output = Path(obj_publish['path'])
    path_code_output = Path(obj_publish['codeGeneration']['codePath'])
    class_name_prefix = obj_publish['codeGeneration']['classNamePrefix']
    if not path_bin_output.is_absolute():
        path_bin_output = path_fgui / path_bin_output
    if not path_code_output.is_absolute():
        path_code_output = path_fgui / path_code_output

    pkg_list = []
    if args.type == 1:  # 等待用户输入
        input_pkg = input('输入你要发布的包名，多个包可用逗号分隔，不填则为输出所有包:')
        if input_pkg:
            pkg_list = input_pkg.split(',')
            print(input_pkg)
    else:  # 参数运行
        if args.pkg:
            pkg_list = args.pkg.split(',')

    # 预加载包列表
    preloads = []
    if args.preload:
        preloads = args.preload.split(',')

    # Copy2Work.run(str(path_bin_output), str(path_code / 'resource' / 'UI'), pkg_list)
    # print(str(path_code_output))
    path_code_target = path_code / 'src' / 'game' / 'uicode'
    # print(str(path_code_target))
    FGUICodeTool.export(str(path_code_output), str(path_code_target), pkg_list)
    Copy2Work2.run(str(path_code_output), str(path_code_target), str(path_fgui / 'assets'), class_name_prefix,
                   pkg_list, preloads)
    # DefaultTool.run(str(path_code))
