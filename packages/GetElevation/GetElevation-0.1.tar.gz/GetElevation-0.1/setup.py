import setuptools

with open("README.md", "r",encoding="utf-8-sig") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GetElevation", # 模块名称
    version = "0.1", # 当前版本
    author="吴镇江", # 作者
    author_email="852356187@qq.com", # 作者邮箱
    description="这是一个批量/单次查询经高程的模块", # 简短介绍
    long_description=long_description, # 模块详细介绍
    long_description_content_type="text/markdown", # 模块详细介绍格式
    packages=setuptools.find_packages(), # 自动找到项目中导入的模块
    # 模块相关的元数据(更多描述信息)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'requests',
        'pandas',
    ],
    python_requires=">=3",
    # url="https://github.com/UncoDong", # github地址
)