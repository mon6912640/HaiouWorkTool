from pathlib import Path
import re

"""
检测代码文件中相同ui url工具
"""


class KeyVo():
    key = ''
    list_path = []
    count = 0

    def __init__(self, p_key, p_list_path):
        self.key = p_key
        self.list_path = p_list_path
        self.count = 0

    def append(self, p_path):
        self.list_path.append(p_path)
        self.count += 1


dir_path = 'D:/work_haiou/branch/sanguo_wechat/src'


def run(p_dir):
    path_dir = Path(p_dir)
    if not path_dir.exists():
        print('指定目录不存在，程序退出')
        return

    vo_map = {}
    mul_map = {}
    mul_count = 0
    list_file = sorted(path_dir.rglob('*.ts'))
    for v in list_file:
        str_code = v.read_text(encoding='utf-8')
        # public static URL: string = "ui://3tzqotadn4tus";
        result = re.search('static URL.+"(ui://\S+)"', string=str_code)
        if result is not None:
            url_key = result.group(1)
            if url_key not in vo_map:
                vo = KeyVo(url_key, [])
                vo_map[url_key] = vo
            else:
                vo = vo_map[url_key]
            vo.append(v)
            if vo.count > 1 and url_key not in mul_map:
                mul_map[url_key] = vo
                mul_count += 1

    print('一共有{0}个url在代码中出现定义重复，列举如下：\n'.format(mul_count))
    for k in mul_map:
        vo = mul_map[k]
        print('url = {0}，共出现了{1}次'.format(vo.key, vo.count))
        for v in vo.list_path:
            print('\t{0}'.format(v.name))


run(dir_path)
