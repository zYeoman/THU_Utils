from io import open

from setuptools import setup
from setuptools import find_packages

with open('thu_utils/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='thu_utils',
    version=version,
    description='THU Utils Tools for tsinghua students ',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Yongwen Zhuang',
    author_email='zyeoman@163.com',
    maintainer='Yongwen Zhuang',
    maintainer_email='zyeoman@163.com',
    url='https://github.com/zYeoman/userpass',
    license='GPLv3',

    keywords=[
        'spider',
        'utils',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPLv3 License',
        'Natural Language :: Chinese',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    package=find_packages(),
    install_requires=['lxml', 'bs4', 'prettytable', 'requests'],

)
