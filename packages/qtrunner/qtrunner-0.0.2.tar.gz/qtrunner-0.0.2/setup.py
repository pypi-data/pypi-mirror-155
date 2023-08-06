#!/usr/bin/env python

from setuptools import setup
import runner

with open("README_CN.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf8") as f:
    requires = f.read()

setup(
    name='qtrunner',
    version=runner.__version__,
    author=runner.__author__,
    author_email=runner.__author_email__,
    url='https://github.com/notmmao/runner',
    description=u'快速命令启动器',
    long_description=long_description,
    packages=['runner'],
    install_requires=requires.splitlines(),
    python_requires=">=3.6",
    platforms="windows",
    license="MIT",
    keywords=["qt", "launcher"],
    include_package_data = True,
    package_data = {
        "" : [
            "*.json"
        ]
    },
    entry_points={
        'console_scripts': [
            'runner=runner:main'
        ]
    }
)
