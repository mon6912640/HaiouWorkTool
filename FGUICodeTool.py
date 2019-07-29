import argparse
import re
from pathlib import Path


def export(p_source, p_export, p_all_in_one=False):
    path_source = Path(p_source)
    path_export = Path(p_export)
    list_file = sorted(path_source.rglob('*.ts'))
    for v in list_file:
        with v.open() as f:
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
                path_target = path_export / v.relative_to(path_source)
                path_target.parent.mkdir(parents=True, exist_ok=True)
                path_target.write_text(output_str)
            else:
                # 处理ui导出类
                def rpl_construct_func(m):
                    result = ''
                    result += '\t\t\tlet s = this;\n'
                    s1 = m.group(1)
                    s2 = m.group(2).lstrip('\n')
                    s3 = m.group(3)
                    result += s2.replace('this', 's')
                    return s1 + '\n' + result + s3

                output_str = re.sub('(super\.constructFromXML\(xml\);)(.+?)(^\s*}\s*$)', rpl_construct_func, str_code,
                                    flags=re.M | re.DOTALL)
                path_target = path_export / v.relative_to(path_source)
                path_target.parent.mkdir(parents=True, exist_ok=True)
                path_target.write_text(output_str)
    print('输出完毕')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='帮助信息')
    parser.add_argument('--source', type=str, default='./fabu', help='fui工程目录')
    parser.add_argument('--output', type=str, default='./fabu2', help='输出的目录')
    args = parser.parse_args()

    export(args.source, args.output)
