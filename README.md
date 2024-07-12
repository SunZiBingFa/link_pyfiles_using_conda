# 批处理: python脚本中使用conda环境

## 简介
#### 主要目的
`[link].py` 的作用是启用某个conda环境来运行目标文件 `[target].py`。
<br>

#### 批处理
获取`[target_folder]`目录下所有的文件，在`[link_folder]`文件夹下创建相同目录结构的文件(可自定义过滤规则) ，生成`[link].py`。
<br>

#### 举个例子
```
# [target_folder] 目标目录结构
├── user_folder_01
    ├── user_1_a.py
    ├── user_1_b.py
├── user_folder_02
    ├── user_1_a.py
    ├── test.py
├── useless_folder
    ├── useless_1.py
    ├── useless_2.py
├── img
    ├── a1.png
    ├── a2.png
├── README.md
├── .git
├── .gitignore
```

```
# 忽略规则：在 config.json 中配置，支持正则表达式
# (自动过滤出文件夹和*.py文件)
ignore_file_or_folder :["^\\.", "img", "test.py", "useless.*"]
```

```
# 生成的 [link_folder] 目录结构
├── user_folder_01
    ├── user_1_a.py
    ├── user_1_b.py
├── user_folder_02
    ├── user_1_a.py
```

一个`[link].py`对应一个`[target].py`，文件名相同，目录结构相同。
`[link].py`的内容如下，变量请在`config.json`中配置
```
import subprocess, os

if __name__ == "__main__":
    full_command = f'source {activate} {env} && python3 "{link_path}"'
    result = subprocess.getoutput(full_command)
    print(result)
```

## 其他功能
备份目标文件夹下的内容，移动到临时文件下。临时文件的路径请在`config.json`中配置。

## 配置内容
这是对`config.json`配置的说明
```
{
    ## conda 环境名
    "env_name": "your_conda_env_name",

    ## activate 的路径, 终端键入 where activate 查看
    "activate_path": "/usr/local/Caskroom/miniconda/base/bin/activate",

    ## 用户py脚本的文件夹路径
    "user_script_path": "~/Documents/Code/DaVinciScript/Scripts",

    ## 链接文件的文件夹路径
    "link_path": "~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Edit",

    ## 忽略文件和文件夹的规则
    "ignore_file_or_folder": ["^\\.", "__pycache__", "img"],

    ## 是否将链接文件路径的内容备份到临时目录
    "is_move_to_temp": true,

    ## 临时目录路径
    "temp_dir": "~/Desktop/temp"
}
```
<br>

## 使用方法
1. 修改`config.json`配置文件
2. 执行`python link_pyfiles_using_conda.py`
<br>

## 用处
- 为了解决用`conda`环境写`DaVinci Resolve`脚本时遇到问题
    - `DaVinci Resolve` 中用软件菜单栏调用py脚本，使用的是系统环境的python
    - 而目录下每个`.py`文件都需要使用conda环境调用
    - 这里我把脚本写得比较通用，也许在别的情况下也有用
