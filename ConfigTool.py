import os
import zlib
from pathlib import Path


def file_compress(spath, tpath, level=9, delete_source=False):
    """
    zlib.compressobj 用来压缩数据流，用于文件传输
    :param spath:源文件
    :param tpath:目标文件
    :param level:压缩等级，越高压缩率越大，对应解压时间也变大
    :param delete_source:是否删除源文件，默认不删除
    :return:
    """
    file_source = open(spath, 'rb')
    file_target = open(tpath, 'wb')
    compress_obj = zlib.compressobj(level, wbits=-15, method=zlib.DEFLATED)  # 压缩对象
    data = file_source.read(1024)  # 1024为读取的size参数
    while data:
        file_target.write(compress_obj.compress(data))  # 写入压缩数据
        data = file_source.read(1024)  # 继续读取文件中的下一个size的内容
    file_target.write(compress_obj.flush())  # compressobj.flush()包含剩余压缩输出的字节对象，将剩余的字节内容写入到目标文件中
    file_source.close()
    file_target.close()
    if delete_source:
        os.remove(spath)


def file_decompress(spath, tpath):
    """
    解压文件
    :param spath:源文件
    :param tpath:目标文件
    :return:
    """
    file_source = open(spath, 'rb')
    file_target = open(tpath, 'wb')
    decompress_obj = zlib.decompressobj(wbits=-15)
    data = file_source.read(1024)
    while data:
        file_target.write(decompress_obj.decompress(data))
        data = file_source.read(1024)
    file_target.write(decompress_obj.flush())
    file_source.close()
    file_target.close()


config_path = 'D:/work_haiou/client/sanguo/bin-release/web/190822200649/resource/config/config0.json'

if __name__ == '__main__':
    path_config = Path(config_path)
    path_zip = path_config.parent / (path_config.name.split('.')[0] + '.zip')
    print(path_zip)
    file_compress(path_config, path_zip)
    pass
