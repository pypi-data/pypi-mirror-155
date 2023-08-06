from setuptools import setup

with open("README.md", "r", encoding='utf8') as f:
    long_description = f.read()

setup(
    name='impython',
    version='0.1.0',
    author='junruoyu-zheng',
    author_email='zhengjry@outlook.com',
    url='https://gitee.com/junruoyu-zheng/impython',
    description=u'impython is a python interpreter that accepts pipe stdin inputs and recognizes some magic commands. ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['impython'],
    install_requires=[],
    entry_points={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)