# -- coding: utf-8 --
# __create_time__ : 2022/6/14 18:04
# __email__: codeCui@outlook.com
# --auth__ : cui
# __file__ : setup.py.py
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="code-cui",  # 模块名称
    version="1.0",  # 当前版本
    author="cui",  # 作者
    author_email="codeCui@outlook.com",  # 作者邮箱
    description="测试包",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'pillow',
        "requests"
    ],
    python_requires='>=3',
)