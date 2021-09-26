import hashlib
def md5(file_path):
#------判断文件的MD5-------↓
    if os.path.isdir(file_path):
        return '1'
    read_file=open(file_path,mode='r',errors='ignore')
 
    the_hash=hashlib.md5()
    for line in read_file.readlines():
        the_hash.update(line.encode('utf8'))
    read_file.close()
    return the_hash.hexdigest()
 
 
import os
import shutil
def directory(dir_name1,dir_name2):
#-------克隆目录1结构到目录2--------↓
    dir1_list=[]
    for path,dirs,files in os.walk(dir_name1):
        # print(path,dirs,files)
        dir1_list.append(path)
    a=len(dir1_list[0])
    for i in range(len(dir1_list)):
        if os.path.exists(dir_name2+dir1_list[i][a:]) is False:
            os.mkdir(dir_name2+dir1_list[i][a:])
    dir2_list=[]
    for path,dirs,files in os.walk(dir_name2):
        dir2_list.append(path)
    a=len(dir2_list[0])
    for i in range(len(dir2_list)):
        if os.path.exists(dir_name1+dir2_list[i][a:]) is False:
            os.rmdir(dir2_list[i]) 
#-------判断目录1哪些文件变更,复制到目录2--------↓
    dir1_root=None
    for path,dirs,files in os.walk(dir_name1):
        if dir1_root is None:
            dir1_root=path
        trimmed_path=path[len(dir1_root):]
        # print(trimmed_path,files)
        if files!=[]:
            for i in range(len(files)):
                file1=os.path.join(dir_name1+trimmed_path+os.path.sep,files[i])
                file2=os.path.join(dir_name2+trimmed_path+os.path.sep,files[i])
                if os.path.exists(file2) is True:
                    if md5(file1) != md5(file2):
                        shutil.copy(file1,file2)
                else:
                    shutil.copy(file1,file2)                    
#-------删除目录2比目录1多出来的文件--------↓
    dir2_root=None
    for path,dirs,files in os.walk(dir_name2):
        if dir2_root is None:
            dir2_root=path
        trimmed_path=path[len(dir2_root):]
        # print(trimmed_path,files)
        if files!=[]:
            for i in range(len(files)):
                if os.path.exists(dir_name1+trimmed_path+os.path.sep+files[i]) is False:
                    os.remove(dir_name2+trimmed_path+os.path.sep+files[i])
 
 
directory('E:\\22','E:\\33')