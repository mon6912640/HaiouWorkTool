import argparse
import re
from pathlib import Path
import shutil


def export(p_source, p_export, p_all_in_one=False):
    path_source = Path(p_source)
    path_export = Path(p_export)
    if path_export.exists():
        shutil.rmtree(str(path_export))
    list_file = sorted(path_source.rglob('*.ts'))
    for v in list_file:
        with v.open(encoding='utf-8') as f:
            str_code = f.read()
            if 'Binder.ts' in v.name:
                # 处理Binder类
                def rpl_bind_func(m):
                    result = ''
                    result += '\t\t\tlet f = fairygui.UIObjectFactory.setPackageItemExtension;\n'
                    s1 = m.group(1)
                    s2 = m.group(2).lstrip('\n')
                    s3 = m.group(3)
                    result += s2.replace('fairygui.UIObjectFactory.setPackageItemExtension', 'f')
                    return s1 + '\n' + result + s3

                output_str = re.sub('(bindAll\(\):void {\s*$)(.+?)(^\s*}\s*$)', rpl_bind_func, str_code,
                                    flags=re.M | re.DOTALL)
            else:
                # 处理ui导出类
                # 替换形式1
                def rpl_construct_func1(m):
                    result = ''
                    result += '\t\t\tlet s = this;\n'
                    s1 = m.group(1)
                    s2 = m.group(2).lstrip('\n')
                    s3 = m.group(3)
                    result += s2.replace('this', 's')
                    return s1 + '\n' + result + s3

                # 替换形式2
                def rpl_construct_func2(m):
                    get_str_map = {}
                    result = ''
                    s1 = m.group(1)
                    s2 = m.group(2).lstrip('\n')
                    s3 = m.group(3)
                    find_list = re.findall('this\.get([^\\\(]+?)\([\'\"](.+?)[\'\"]\)', s2, flags=re.M)
                    for v in find_list:
                        if v[0] not in get_str_map:
                            get_str_map[v[0]] = []
                        get_str_map[v[0]].append(v[1])
                    for k, v in get_str_map.items():
                        list_name = k
                        list_str = ''
                        for pname in v:
                            list_str += '"{0}",'.format(pname)
                        result += '\n\t\t\tlet {0} = [{1}];\n' \
                                  '\t\t\tfor(let i = 0; i<{0}.length; i++)\n' \
                                  '\t\t\t\tthis[{0}[i]] = <any>this.get{0}({0}[i]);\n'.format(list_name, list_str)
                    return s1 + '\n' + result + s3

                output_str = re.sub('(super\.constructFromXML\(xml\);)(.+?)(^\s*}\s*$)', rpl_construct_func2, str_code,
                                    flags=re.M | re.DOTALL)

            path_target = path_export / v.relative_to(path_source)
            path_target.parent.mkdir(parents=True, exist_ok=True)
            path_target.write_text(output_str, encoding='utf-8')
    print('输出完毕')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='帮助信息')
    parser.add_argument('--source', type=str, default='./fabu', help='fui工程目录')
    parser.add_argument('--output', type=str, default='./fabu2', help='输出的目录')
    args = parser.parse_args()

    export(args.source, args.output)
