#!/usr/local/bin/python3
import os
import re
import shutil
import json


def get_context(env, activate, link_path):
    context = f"""\
import subprocess, os

if __name__ == "__main__":
    full_command = f'source {activate} {env} && python3 "{link_path}"'
    result = subprocess.getoutput(full_command)
    print(result)
"""
    return context


def move_contents_to_temp(temp_dir, dst_path):
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    for root, dirs, files in os.walk(dst_path):
        relative_path = os.path.relpath(root, dst_path)
        target_path = os.path.join(temp_dir, relative_path)
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_path, file)
            shutil.move(src_file, dst_file)

    for root, dirs, files in os.walk(dst_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                os.rmdir(dir_path)  # 删除空目录
            except OSError:
                pass
    
def create_filtered_structure(env, activate, src_path, dst_path, ignore_patterns):
    """
    根据源路径的目录结构，在目标路径下创建对应的目录和空文件，
    同时根据过滤规则忽略特定的文件和目录。
    
    :param src_path: str, 源目录路径
    :param dst_path: str, 目标目录路径
    :param ignore_patterns: list, 需要忽略的文件/目录名模式列表
    """
    
    # 编译正则表达式
    ignore_compiled = [re.compile(pattern) for pattern in ignore_patterns]
    
    def should_ignore(name):
        """判断一个文件或目录是否应该被忽略"""
        for pattern in ignore_compiled:
            if pattern.match(name):
                return True
        return False

    def copy_dir_structure_and_link(env, activate, src, dst):
        os.makedirs(dst, exist_ok=True)
        for item in os.listdir(src):
            if should_ignore(item):
                continue
            src_item = os.path.join(src, item)
            dst_item = os.path.join(dst, item)
            if os.path.isfile(src_item) and not src_item.endswith('.py'): ## 过滤文件类型 仅.py文件 和 文件夹
                continue
            if os.path.isdir(src_item):
                copy_dir_structure_and_link(env, activate, src_item, dst_item)
            else:  # 文件
                context = get_context(env, activate, src_item)
                with open(dst_item, 'w') as file:
                    file.write(context)

    copy_dir_structure_and_link(env, activate, src_path, dst_path)


def read_config_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        config_data = json.load(file)
    return config_data

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_json_path = os.path.join(script_dir, 'config.json')
    config_data = read_config_from_json(config_json_path)

    env = config_data['env_name']
    activate = config_data['activate_path']
    src_path = os.path.expanduser(config_data['user_script_path'])
    dst_path = os.path.expanduser(config_data['link_path'])
    ignore_list = config_data['ignore_file_or_folder']
    is_move_to_temp = config_data['is_move_to_temp']
    temp_dir = os.path.expanduser(config_data['temp_dir'])

    if is_move_to_temp:
        move_contents_to_temp(temp_dir, dst_path)  ## 移动到临时文件夹(备份)

    create_filtered_structure(env, activate, src_path, dst_path, ignore_list)

if __name__ == "__main__":
    main()