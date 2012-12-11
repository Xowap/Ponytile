# vim: fileencoding=utf8 tw=120 expandtab ts=4 sw=4 :

# Ponytile
# Setup file.
#
# Copyright (c) 2012 Rémy Sanchez <remy.sanchez@hyperthese.net>
# Under the terms of the WTFPL

from distutils.core import setup

setup(
    name='Ponytile',
    version='0.1.1',
    author='Rémy Sanchez',
    author_email='remy.sanchez@hyperthese.net',
    packages=['ponytile'],
    scripts=['bin/ponytile'],
    url='https://github.com/Xowap/Ponytile',
    license='LICENSE.txt',
    description='A library bundled with a CLI tool to generate CSS sprites.',
    long_description=open('README.rst').read(),
    install_requires=[
        "Pillow >= 1.0",
    ],
)
