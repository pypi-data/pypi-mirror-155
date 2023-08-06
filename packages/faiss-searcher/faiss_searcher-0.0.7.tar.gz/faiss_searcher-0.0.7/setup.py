from os import path
from setuptools import setup, find_packages  # 这个包没有的可以pip一下

here = path.abspath(path.dirname(__file__))

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    long_description = ""

setup(
    name="faiss_searcher",  # 这里是pip项目发布的名称
    version="0.0.7",  # 版本号，数值大的会优先被pip
    keywords=["pip", "faiss_searcher"],  # 关键字
    description="基于Pandas的Faiss检索小工具",  # 描述
    long_description="基于Pandas的Faiss检索小工具",
    license="MIT",  # 许可证

    url="https://github.com/mechsihao/FaissSearcher",  # 项目相关文件地址，一般是github项目地址即可
    author="MECH",  # 作者
    author_email="sihaomech@icloud.com",

    classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: System :: Logging',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
    py_modules=["faiss_searcher"],
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "pandas>=1.3.0", "bert4keras==0.10.8", "tensorflow"
    ]  # 这个项目依赖的第三方库
)
