from pathlib import Path

import logging

import tcod.tileset
from tcod.tileset import CHARMAP_CP437, CHARMAP_TCOD, Tileset

tileset_params = dict((
    ("arial10x10.png",                  (32, 8,  CHARMAP_TCOD)),
    ("arial12x12.png",                  (32, 8,  CHARMAP_TCOD)),
    ("arial8x8.png",                    (32, 8,  CHARMAP_TCOD)),
    ("caeldera8x8_gs_tc.png",           (32, 8,  CHARMAP_TCOD)),
    ("celtic_garamond_10x10_gs_tc.png", (32, 8,  CHARMAP_TCOD)),
    ("consolas10x10_gs_tc.png",         (32, 8,  CHARMAP_TCOD)),
    ("consolas12x12_gs_tc.png",         (32, 8,  CHARMAP_TCOD)),
    ("consolas8x8_gs_tc.png",           (32, 8,  CHARMAP_TCOD)),
    ("courier10x10_aa_tc.png",          (32, 8,  CHARMAP_TCOD)),
    ("courier12x12_aa_tc.png",          (32, 8,  CHARMAP_TCOD)),
    ("courier8x8_aa_tc.png",            (32, 8,  CHARMAP_TCOD)),
    ("dejavu10x10_gs_tc.png",           (32, 8,  CHARMAP_TCOD)),
    ("dejavu12x12_gs_tc.png",           (32, 8,  CHARMAP_TCOD)),
    ("dejavu16x16_gs_tc.png",           (32, 8,  CHARMAP_TCOD)),
    ("dejavu8x8_gs_tc.png",             (32, 8,  CHARMAP_TCOD)),
    ("dejavu_wide12x12_gs_tc.png",      (32, 8,  CHARMAP_TCOD)),
    ("dejavu_wide16x16_gs_tc.png",      (32, 8,  CHARMAP_TCOD)),
    ("dundalk12x12_gs_tc.png",          (32, 8,  CHARMAP_TCOD)),
    ("lucida10x10_gs_tc.png",           (32, 8,  CHARMAP_TCOD)),
    ("lucida12x12_gs_tc.png",           (32, 8,  CHARMAP_TCOD)),
    ("lucida8x8_gs_tc.png",             (32, 8,  CHARMAP_TCOD)),
    ("prestige10x10_gs_tc.png",         (32, 8,  CHARMAP_TCOD)),
    ("prestige12x12_gs_tc.png",         (32, 8,  CHARMAP_TCOD)),
    ("prestige8x8_gs_tc.png",           (32, 8,  CHARMAP_TCOD)),
    ("terminal10x10_gs_tc.png",         (32, 8,  CHARMAP_TCOD)),
    ("terminal10x16_gs_ro.png",         (16, 16, CHARMAP_CP437)),
    ("terminal10x16_gs_tc.png",         (32, 8,  CHARMAP_TCOD)),
    ("terminal10x18_gs_ro.png",         (16, 16, CHARMAP_CP437)),
    ("terminal12x12_gs_ro.png",         (16, 16, CHARMAP_CP437)),
    ("terminal16x16_gs_ro.png",         (16, 16, CHARMAP_CP437)),
    ("terminal7x7_gs_tc.png",           (32, 8,  CHARMAP_TCOD)),
    ("terminal8x12_gs_ro.png",          (16, 16, CHARMAP_CP437)),
    ("terminal8x12_gs_tc.png",          (32, 8,  CHARMAP_TCOD)),
    ("terminal8x14_gs_ro.png",          (16, 16, CHARMAP_CP437)),
    ("terminal8x8_gs_ro.png",           (16, 16, CHARMAP_CP437)),
    ("terminal8x8_gs_tc.png",           (32, 8,  CHARMAP_TCOD)),
    # ("terminal8x8_aa_as.png",           (16, 16, CHARMAP_TCOD)),
    # ("terminal8x8_aa_ro.png",           (16, 16, CHARMAP_TCOD)),
    # ("terminal8x8_aa_tc.png",           (32, 8,  CHARMAP_TCOD)),
    # ("terminal8x8_gs_as.png",           (16, 16, CHARMAP_TCOD)),
    # ("consolas_unicode_10x10.png",      (32, 32, CHARMAP_TCOD)),
    # ("consolas_unicode_12x12.png",      (32, 32, CHARMAP_TCOD)),
    # ("consolas_unicode_16x16.png",      (32, 32, CHARMAP_TCOD)),
    # ("consolas_unicode_8x8.png",        (32, 32, CHARMAP_TCOD)),
))

tileset_indexes = [filename for filename in tileset_params.keys()]

def get_tileset(filename: str) -> Tileset:
    path = Path("resources", "fonts", filename)
    return tcod.tileset.load_tilesheet(path, *tileset_params[filename])

def get_index_and_tileset(filename: str) -> tuple[int, Tileset]:
    idx = tileset_indexes.index(filename)
    return idx, get_tileset(filename)

def get_tileset_by_index(idx: int) -> tuple[str, Tileset]:
    tileset_name = tileset_indexes[idx % len(tileset_indexes)]
    return tileset_name, get_tileset(tileset_name)

def get_bdf_tileset(idx: int) -> tuple[str, Tileset]:
    bdfs = list(Path("resources", "fonts", "bdf").glob("*.bdf"))
    bdf = bdfs[idx % len(bdfs)]
    logging.debug(bdf.name)
    return bdf.name, tcod.tileset.load_bdf(bdf)
