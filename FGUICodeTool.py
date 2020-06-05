import argparse
import re
from pathlib import Path
import shutil


def export(p_source, p_export, p_pkg_list=None):
    path_source = Path(p_source)
    path_export = Path(p_export)

    if not path_source.exists():
        print('源目录不存在，程序退出')
        return
    if path_source.absolute() == path_export.absolute():
        print('源目录和目标输出目录不能相同！')
        return

    if p_pkg_list is None or len(p_pkg_list) == 0:
        is_all = True
        print('本次将输出全部包')
    else:
        is_all = False
        print('本次将输出{0}个包'.format(len(p_pkg_list)), p_pkg_list)

    # 清理输出目录（要区分全部清理还是只清理指定的包）
    # if is_all:
    #     if path_export.exists():
    #         shutil.rmtree(str(path_export))
    # else:
    #     for v in pkg_list:
    #         path_pkg_dir = path_export / v
    #         if path_pkg_dir.exists():
    #             shutil.rmtree(str(path_pkg_dir))

    total_count = 0

    list_file = sorted(path_source.rglob('*.ts'))
    for v in list_file:
        # 包名（所在目录名称）
        pkg = v.parent.name
        if not is_all and pkg not in p_pkg_list:
            continue
        write_flag = False
        with v.open(encoding='utf-8') as f:
            str_source = f.read()
            path_target = path_export / v.relative_to(path_source)
            path_target.parent.mkdir(parents=True, exist_ok=True)
            if 'Binder.ts' in v.name:
                # 处理Binder类
                write_flag = True

                def rpl_bind_func(m):
                    result = ''
                    result += '\t\t\tlet f = fairygui.UIObjectFactory.setPackageItemExtension;\n'
                    s1 = m.group(1)
                    s2 = m.group(2).lstrip('\n')
                    s3 = m.group(3)
                    result += s2.replace('fairygui.UIObjectFactory.setPackageItemExtension', 'f')
                    return s1 + '\n' + result + s3

                output_str = re.sub('(bindAll\(\):void {\s*$)(.+?)(^\s*}\s*$)', rpl_bind_func, str_source,
                                    flags=re.M | re.DOTALL)
            else:
                output_str = str_source
                if path_target.exists():
                    # 读取已经存在的文件
                    m_source = re.search('(extends\s+)(.+?)(\s+)', str_source, flags=re.M | re.DOTALL)
                    if m_source:
                        with path_target.open(encoding='utf-8') as fe:
                            str_fe = fe.read()
                            # 匹配出的扩展类型
                            str_extends = m_source.group(2)

                            def rpl_extends(m):
                                s1 = m.group(1)
                                s2 = m.group(2)
                                s3 = m.group(3)
                                return s1 + str_extends + s3

                            output_str = re.sub('(extends\s+)(.+?)(\s+)', rpl_extends, str_fe,
                                                flags=re.M | re.DOTALL)
                            if output_str != str_fe:
                                write_flag = True
                else:
                    write_flag = True
                    output_str = str_source

                # # 处理ui导出类
                # # 替换形式1
                # def rpl_construct_func1(m):
                #     result = ''
                #     result += '\t\t\tlet s = this;\n'
                #     s1 = m.group(1)
                #     s2 = m.group(2).lstrip('\n')
                #     s3 = m.group(3)
                #     result += s2.replace('this', 's')
                #     return s1 + '\n' + result + s3
                #
                # # 替换形式2
                # def rpl_construct_func2(m):
                #     get_str_map = {}
                #     result = ''
                #     s1 = m.group(1)
                #     s2 = m.group(2).lstrip('\n')
                #     s3 = m.group(3)
                #     find_list = re.findall('this\.get([^\\\(]+?)\([\'\"](.+?)[\'\"]\)', s2, flags=re.M)
                #     for v in find_list:
                #         if v[0] not in get_str_map:
                #             get_str_map[v[0]] = []
                #         get_str_map[v[0]].append(v[1])
                #     for k, v in get_str_map.items():
                #         list_name = k
                #         list_str = ''
                #         for pname in v:
                #             list_str += '"{0}",'.format(pname)
                #         result += '\n\t\t\tlet {0} = [{1}];\n' \
                #                   '\t\t\tfor(let i = 0; i<{0}.length; i++)\n' \
                #                   '\t\t\t\tthis[{0}[i]] = <any>this.get{0}({0}[i]);\n'.format(list_name, list_str)
                #     return s1 + '\n' + result + s3
                #
                # output_str = re.sub('(super\.constructFromXML\(xml\);)(.+?)(^\s*}\s*$)', rpl_construct_func2, str_source,
                #                     flags=re.M | re.DOTALL)

            if write_flag:
                path_target.write_text(output_str, encoding='utf-8')
                total_count += 1
    print('输出完毕，共处理了{0}个文件'.format(total_count))


# # 配置
# path_config = Path('./FGUICodeTool_cfg.json')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='帮助信息')
    parser.add_argument('--type', type=int, default=0, help='运行类型 0：参数运行 1：等待用户输入')
    parser.add_argument('--source', type=str, default='./fabu', help='fui工程目录')
    parser.add_argument('--output', type=str, default='./fabu2', help='输出的目录')
    parser.add_argument('--pkg', type=str, default='', help='指定的包名称列表，用逗号分隔，默认为空则为输出所有包')
    args = parser.parse_args()

    print('---- 运行发布精简代码的脚本')
    pkg_list = []
    if args.type == 1:  # 等待用户输入
        input_pkg = input('输入你要发布的包名，多个包可用逗号分隔，不填则为输出所有包，回车键确定:')
        if input_pkg:
            pkg_list = input_pkg.split(',')
    else:  # 参数运行
        if args.pkg:
            pkg_list = args.pkg.split(',')

    export(args.source, args.output, pkg_list)
