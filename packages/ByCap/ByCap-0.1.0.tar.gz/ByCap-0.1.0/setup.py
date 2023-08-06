from setuptools import setup, find_packages

classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name                 = 'ByCap',
    version              = '0.1.0',
    description          = 'A simple python library that bypasses captchas.',
    long_description = long_description,
    author               = 'Jiro',
    author_email         = 'contact@jiroawesome.tech',
    url                  = '',
    py_modules           = ['ByCap/__init__', 'ByCap/base', 'ByCap/compat', 'ByCap/exceptions', 'ByCap/tasks'],
    license              = 'MIT',
    include_package_data = True
    )