Running pyrl
============
Execute either pyrl.py or sdlpyrl.py depending on your platform/environment

### Windows requirements

#### 32-bit Python 2.7
Execute sdlpyrl.py to start
(No ncurses variant available)

### *nix requirements

#### Python 2.7 32-bit and SDL
Execute sdlpyrl.py to start

#### Python 2.7 and ncurses
Execute pyrl.py in a terminal emulator to start

### Mac requirements

#### Python 2.7 and ncurses
Execute pyrl.py in a terminal emulator to start


Installing SDL
--------------

### Ubuntu
    sudo apt-get install libsdl1.2

### Debian (is usually preinstalled, but)
    sudo apt-get install libsdl1.2debian

### Windows
    comes bundled with the game


Ncurses specific issues
=======================

Information given under this paragraph is only relevant when using the terminal
version of the game, ie. when running pyrl.py

More colors
-----------

pyrl.py supports 256 colors for more variety. To use this feature set your
TERM entry to xterm-256color (or other, see below). Some terminals allow to
do this in their settings, but others (like gnome-terminal and Terminal)
hardcode it (also see below). You can always force the TERM from the command
line by writing the following

    export TERM=xterm-256color

ncurses-term
------------

ncurses-term is a package that adds more termcap entries which allows for
more compatibility for many terminals. If the package is installed your
machine you can instead use one of the following entries for your TERM for
better compatibility for your particular terminal

### Some terminals and their corresponding TERM values

* putty              putty-256color
* gnome-terminal     gnome-256color
* Terminal           gnome-256color
* Konsole            konsole-256color
* rxvt               rxvt-256color
* xterm              xterm-256color

Using a correct TERM entry allows for maximum compatibility. Some terminals
default to xterm even if it doesn't reflect their functionality which has
the side effect of making some keys not work (numpad-, F-, and Home/End keys
are often keys that have problems)

### gnome-terminal and Terminal

Because gnome-terminal and Terminal hardcode the TERM to be xterm
another way of setting the term is needed. The following shell snippet
changes the term to be what it needs to be when gnome-terminal or
Terminal are used but doesn't affect other terminals. Put these snippets
into your .bashrc or equivalent

    if [[ "$TERM" = "xterm" && "$COLORTERM" = "gnome-terminal" ]]; then
        export TERM=gnome-256color
    fi

    if [[ "$TERM" = "xterm" && "$COLORTERM" = "Terminal" ]]; then
        export TERM=gnome-256color
    fi

### without ncurses-term

If you set your term to xterm-256color you'll get the colors you want. You
can also optionally run pyrl under screen which can bridge compatibility and
make more keys work. This is because screen doesn't blindly believe the TERM
entry but does under the hood investigating to fix stuff.
Remember to set the following in your .screenrc

    term "screen-256color"


### About ESC
The game doesn't require the user to use ESC when playing the game because
of the one second default delay that some terminals have. If you wish to use
ESC when running pyrl.py without a considerable delay you can set the
environmental variable ESCDELAY a value of your choosing in milliseconds. To
set the value do the following in the command line or .bashrc (or
equivalent)

    export ESCDELAY=25
