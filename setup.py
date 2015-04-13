from __future__ import absolute_import, division, print_function, unicode_literals

from distutils.core import setup


setup(
    name='pyrl',
    description='Python roguelike game',
    author='Tapani "tappi" Kiiskinen',
    author_email='tapani.kiiskinen@gmail.com',
    url='http://iridian.fixme.fi/~tappi/pyrl-alpha.tar.gz',
    version='alpha',
    packages=['', 'config', 'const', 'io_wrappers', 'libtcod', 'profile_util', 'templates', 'tests', 'user_input', 'window'],
    platforms=['windows', 'unix', 'mac', 'anything with python 2.7 and curses'],
    license="Creative Commons Attribution-NonCommercial-Sharelike 3.0 Unported License",
    data_files=[
        ('data', ['data/terminal10x18_gs_ro.png']),
        ('', ['docs/LIBTCOD-LICENSE.txt', 'docs/PYRL-LICENSE.txt', 'docs/README', 'docs/glossary', 'libtcod/libtcod.so', 'SDL.dll', 'libtcod/libtcod-mingw.dll', ]),
    ]
)
