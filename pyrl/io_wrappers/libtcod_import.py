def import_libtcod():
    try:
        import libtcod.libtcodpy as libtcod
        return libtcod
    except Exception as e:
        import sys
        print(e, file=sys.stderr)
        print("\nCouldn't load libtcod. Tried both 64-bit and 32-bit libs.", file=sys.stderr)
        print("It's possible this happens because libsdl isn't installed.", file=sys.stderr)
        sys.exit(1)

