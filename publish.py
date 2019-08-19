import Copy2Work
import Copy2Work2
import argparse
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='帮助信息')
    parser.add_argument('--type', type=int, default=0, help='运行类型 0：参数运行 1：等待用户输入')
    parser.add_argument('--pkg', type=str, default='', help='指定的包名称列表，用逗号分隔，默认为空则为输出所有包')

    parser.add_argument('--code', type=str, default='', help='代码工程目录')
    parser.add_argument('--fgui', type=str, default='./src', help='fgui工程目录')

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

    if not args.fgui:
        print('请指定fgui的工程目录')
        exit()

    if not args.code:
        print('请指定代码工程目录')
        exit()

    path_code = Path(args.code)
    if not path_code.exists():
        print('代码工程目录不存在')
        exit()

    file_egret = path_code / 'egretProperties.json'
    if not file_egret.exists():
        print('指定的代码工程目录非Egret工程')
        exit()

    path_fgui = Path(args.fgui)
    if not path_fgui.exists():
        print('fgui工程目录不存在')
        exit()

    file_fgui = path_fgui / 'sanguoUI.fairy'
    if not file_fgui.exists():
        print('指定的fgui工程目录错误')
        exit()

    Copy2Work.run(str(path_fgui / 'fabu'), str(path_code / 'resource' / 'UI'), pkg_list)
    Copy2Work2.run(str(path_fgui / 'fabu'), str(path_code / 'src'), str(path_fgui / 'assets'), pkg_list)
