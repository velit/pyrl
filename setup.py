from distutils.core import setup

setup(
    name='pyrl',
    description='Python roguelike game',
    author='Tapani "tappi" Kiiskinen',
    author_email='tapani.kiiskinen@gmail.com',
    url='http://iridian.fixme.fi/~tappi/pyrl-alpha.tar.gz',
    version='alpha',
    platforms=['windows', 'unix', 'mac', 'anything with python 3.4 and curses'],
    license="Creative Commons Attribution-NonCommercial-Sharelike 3.0 Unported License",
    data_files=[
        ('resources', ['resources/terminal10x18_gs_ro.png']),
        ('', ['docs/LIBTCOD-LICENSE.txt', 'docs/PYRL-LICENSE.txt', 'docs/README', 'docs/glossary', 'libtcod/libtcod.so', 'SDL.dll', 'libtcod/libtcod-mingw.dll', ]),
    ]
)
