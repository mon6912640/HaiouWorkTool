from pathlib import Path

"""
遍历搜索svn目录
"""

source_path = 'D:/work'
path_source = Path(source_path)

list_file = sorted(path_source.rglob('.svn'))
for v in list_file:
    print(str(v))
