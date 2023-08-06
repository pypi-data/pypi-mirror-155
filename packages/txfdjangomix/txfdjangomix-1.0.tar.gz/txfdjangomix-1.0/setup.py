from setuptools import setup, find_packages

setup(name='txfdjangomix',  # 名字
      version='1.0',  # 版本
      description='django response middleware',  # 简介一般我们放在readme.md
      classifiers=[
          'Programming Language :: Python',  # python
          'Intended Audience :: Developers',  # 受众人
          'Operating System :: OS Independent',  # 系统
      ],
      long_description_content_type="text/markdown",  # 类型
      long_description='', # 描述

      url='https://github.com/txf402066270/txfdjangomix/',  # git的目录
      author='wu-di-tian-ge-ge',  # 作者
      author_email='402066270@qq.com',  # 邮箱方便交流
      license='NEU',  # 
      packages=find_packages(),  # 默认
      zip_safe=True,  # 默认
      install_requires=['django', 'djangorestframework']  # 需要的包
      )