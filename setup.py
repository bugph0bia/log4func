import setuptools

from __version__ import __version__


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='log4func',
    version=__version__,
    author='bugph0bia',
    author_email='',
    description='logging helper for functions and methods',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/bugph0bia/log4func',
    packages=setuptools.find_packages(),
    license='MIT',
    keywords='',
    classifiers=[
        'Topic :: System :: Logging',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
    ],
    install_requires=[
    ],
)
