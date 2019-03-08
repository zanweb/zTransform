import os


def is_sub_string(sub_str_list, str):
    """''
    #判断字符串Str是否包含序列sub_str_list中的每一个子字符串
    #>>>sub_str_list=['F','EMS','txt']
    #>>>Str='F06925EMS91.txt'
    #>>>is_sub_string(SubStrList,Str)#return True (or False)
    """
    flag = True
    for sub_str in sub_str_list:
        if not (sub_str in str):
            flag = False

    return flag


def get_file_list(find_path, flag_str=[]):
    """''
    #获取目录中指定的文件名
    #>>>flag_str=['F','EMS','txt'] #要求文件名称中包含这些字符
    #>>>file_list=GetFileList(FindPath,FlagStr) #
    """
    file_list = []
    file_names = os.listdir(find_path)
    if len(file_names) > 0:
        for fn in file_names:
            if len(flag_str) > 0:
                # 返回指定类型的文件名
                if is_sub_string(flag_str, fn):
                    full_file_name = os.path.join(find_path, fn)
                    file_list.append(full_file_name)
            else:
                # 默认直接返回所有文件名
                full_file_name = os.path.join(find_path, fn)
                file_list.append(full_file_name)

                # 对文件名排序
    if len(file_list) > 0:
        file_list.sort()

    return file_list


def get_indicate_ext_file(path, ext):
    """ 获取指定目录下的所有指定后缀的文件名 """
    ext = '.' + str(ext)
    file_name_list = []
    f_list = os.listdir(path)
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == ext:
            file_name_list.append(os.path.splitext(i)[0])
    if file_name_list:
        return file_name_list
    else:
        return


if __name__ == '__main__':
    file_name = get_indicate_ext_file('E:\Zanweb\PythonProgram\Batch\Zfile', 'csv')
    print(file_name)
