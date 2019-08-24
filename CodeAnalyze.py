from pathlib import Path
import re

code_path = 'D:/work_haiou/branch/sanguo_wechat/src/game'


def run(p_code):
    path_code = Path(p_code)
    list_file = sorted(path_code.rglob('*.ts'))
    count = 0
    line_count = 0
    no_match_count = 0
    for v in list_file:
        str_code = v.read_text(encoding='utf-8')
        url_match = re.search('fairygui\.UIPackage\.createObject\("(\w+)", *"(\w+)"\)', string=str_code)
        if url_match is None:
            continue
        count += 1
        diff_flag = False
        pkg = url_match.group(1)
        com = url_match.group(2)
        # print(pkg, com, v.name)
        match_flag = False
        # (?<=this|self)\.(\w+) *=.+(?<=this|view|self)\.getChild\("(\w+)"\)
        items = re.finditer('\w+\.(\w+) *=.+\W\w+\.getChild\("(\w+)"\)', string=str_code)
        if items:
            for m in items:
                # print(m.group(0))
                match_flag = True
                line_count += 1
                pro_name = m.group(1)
                fgui_name = m.group(2)
                if pro_name != fgui_name:
                    diff_flag = True
                    print('出现不一致的变量名赋值操作 {0} === {1} - {2}'.format(v.name, pro_name, fgui_name))
        if diff_flag:
            print('\t来自 {0} | 包 {1} -> {2}\n'.format(v.name, pkg, com))
            pass
        if not match_flag:
            no_match_count += 1
            # print('匹配规则以外 {0}'.format(v.name))
    print('本次遍历了{0}个ts文件，共有{1}行冗余代码，{2}个未匹配文件'.format(count, line_count, no_match_count))


run(code_path)
