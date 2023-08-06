import setuptools
setuptools.setup(
    name="jianxin",  # 自定义工具包的名字
    version="2.0",  # 版本号
    author="liweiren",  # 作者名字
    author_email="niuledabi@qq.com",  # 作者邮箱
    license='MIT',  # 许可协议
    url="https://pypi.org/",  # 项目开源地址
    packages=setuptools.find_packages(),  #自动发现自定义工具包中的所有   包和  子包
)