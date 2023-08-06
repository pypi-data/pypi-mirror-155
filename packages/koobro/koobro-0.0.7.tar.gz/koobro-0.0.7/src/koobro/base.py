import os


def output(value, sep='-----'):
    """
    输出变量信息

    :param value: 变量
    :param sep: 分隔符
    :return:
    """
    # if sep == '\n':
    #     print(f'表达式：{repr(value)} {sep}类型：{type(value)} {sep}值：{value}')
    # else:
    #     print(f'表达式：{repr(value)} {sep} 类型：{type(value)} {sep} 值：{value}')

    if sep == '\n':
        print(f'类型：{type(value)} {sep}值：{value}')
    else:
        print(f'类型：{type(value)} {sep} 值：{value}')


def create_dir(dir_path):
    """
    如果目录不存在，则创建目录

    :param dir_path: 目录路径
    :return:
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
