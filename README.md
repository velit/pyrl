pyrl
====

<a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-nc/3.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/InteractiveResource" property="dct:title" rel="dct:type">pyrl</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/velit/pyrl" property="cc:attributionName" rel="cc:attributionURL">Veli Tapani Kiiskinen</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/">Creative Commons Attribution-NonCommercial 3.0 Unported License</a>.

Running pyrl
============

Execute either 'pyrl.py' or 'sdlpyrl.py' depending on if you want the ncurses or
sdl version of the game. Windows only has support for the sdl version.

### Windows sdlpyrl.py requirements

* 32-bit Python 2.7

### \*nix sdlpyrl.py requirements

* Python 2.7 32-bit
* libSDL

### \*nix and Mac pyrl.py requirements

* Python 2.7
* libncurses
* A terminal or a terminal emulator


Installing SDL
--------------

A .dll for SDL comes bundled with the game on windows.

### Ubuntu
    sudo apt-get install libsdl1.2

### Debian
    sudo apt-get install libsdl1.2debian


Ncurses specific issues
=======================

Information in this paragraph is only relevant when using the terminal version
of the game, ie. when using 'pyrl.py'.

More colors
-----------

pyrl.py supports 256 colors for more variety. To use this feature set your TERM
entry to xterm-256color (or other, see below). Some terminals allow to do this
in their settings, but others (like gnome-terminal and Terminal) hardcode it
(also see below). You can always force the TERM from the command line by writing
the following

    export TERM=xterm-256color

ncurses-term
------------

ncurses-term is a package that adds more termcap entries which allows for more
compatibility for many terminals. If the package is installed your machine you
can instead use one of the following entries for your TERM for better
compatibility for your particular terminal

### Some terminals and their corresponding TERM values

<table>
    <tr>
        <th>Terminal name</th>
        <th>TERM value</th>
    </tr>
    <tr>
        <td>putty</td>
        <td>putty-256color</td>
    </tr>
    <tr>
        <td>gnome-terminal</td>
        <td>gnome-256color</td>
    </tr>
    <tr>
        <td>Terminal</td>
        <td>gnome-256color</td>
    </tr>
    <tr>
        <td>Konsole</td>
        <td>konsole-256color</td>
    </tr>
    <tr>
        <td>rxvt</td>
        <td>rxvt-256color</td>
    </tr>
    <tr>
        <td>xterm</td>
        <td>xterm-256color</td>
    </tr>
</table>

Using a correct TERM entry allows for maximum compatibility. Some terminals
default to xterm even if it doesn't reflect their functionality which has the
side effect of making some keys not work (numpad-, F-, and Home/End keys are
often keys that have problems)

### gnome-terminal and Terminal

Because gnome-terminal and Terminal hardcode the TERM to be xterm another way of
setting the term is needed. The following shell snippet changes the term to be
what it needs to be when gnome-terminal or Terminal are used but doesn't affect
other terminals. Put these snippets into your .bashrc or equivalent

    if [[ "$TERM" = "xterm" && "$COLORTERM" = "gnome-terminal" ]]; then
        export TERM=gnome-256color
    fi

    if [[ "$TERM" = "xterm" && "$COLORTERM" = "Terminal" ]]; then
        export TERM=gnome-256color
    fi

### without ncurses-term

If you set your term to xterm-256color you'll get the colors you want. You can
also optionally run pyrl under screen which can bridge compatibility and make
more keys work. This is because screen doesn't blindly believe the TERM entry
but does under the hood investigating to fix stuff.  Remember to set the
following in your .screenrc

    term "screen-256color"


### About ESC

The game doesn't require the user to use ESC when playing the game because of
the one second default delay that some terminals have. If you wish to use ESC
when using 'pyrl.py' without a considerable delay you can set the environmental
variable ESCDELAY a value of your choosing in milliseconds. To set the value do
the following in the command line or .bashrc (or equivalent)

    export ESCDELAY=25
