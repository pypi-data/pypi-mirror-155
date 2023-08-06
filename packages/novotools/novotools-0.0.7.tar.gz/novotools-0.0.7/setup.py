import setuptools
from setuptools import setup

with open('README.md','r',encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name = "novotools",
    version = "0.0.7",
    packages = setuptools.find_packages(),
    url = "https://github.com/pypa/novotools",
    license = 'MIT',
    author = "chenming",
    author_email = "chenming@novogene.com",
    description = "a common tools to facilitate your coding",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    install_requires = ["python-docx","requests","colorama","openpyxl","click"],
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.8"],
    python_requires = ">=3.8",
    scripts = ["novotools/tools/excel2text.py",
               "novotools/tools/text2excel.py",
               "novotools/tools/getcol.py"],
)