from pathlib import Path
import re


def replace(p_soure, p_export):
    path_source = Path(p_soure)
    path_export = Path(p_export)

    total_count = 0
    list_file = sorted(path_source.rglob('*.ts'))
    for v in list_file:
        with v.open(encoding='utf-8') as f:
            def rpl_func(m):
                result = ''
                s1 = m.group(1)
                # print(s1)
                return result

            str_code = f.read()
            # print(str_code)
            # str_output = re.sub('export (.+)(})', rpl_func, str_code, flags=re.M | re.DOTALL)
            m = re.search('export (.+)}', str_code, flags=re.M | re.DOTALL)
            if m:
                str_output = m.group(1)
                path_target = path_export / v.relative_to(path_source)
                path_target.parent.mkdir(parents=True, exist_ok=True)
                path_target.write_text(str_output, encoding='utf-8')
                total_count += 1
    print('输出完毕，共处理了{0}个文件'.format(total_count))


url_soure = 'C:/Users/Administrator/Desktop/uicode'
url_target = 'C:/Users/Administrator/Desktop/uicode_target'

replace(url_soure, url_target)
