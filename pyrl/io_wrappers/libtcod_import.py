def import_libtcod():

    # noinspection PyBroadException
    try:
        import tcod
        return tcod
    except Exception:
        pass

    try:
        import libtcod.libtcodpy
        return libtcod.libtcodpy
    except Exception as e:
        import sys
        print(e, file=sys.stderr)
        print("\nCouldn't load tcod or libtcod. Tried both 64-bit and 32-bit libs.",
              "It's possible this happens because neither tcod or libsdl isn't installed.",
              sep="\n",
              file=sys.stderr)
        sys.exit(1)
