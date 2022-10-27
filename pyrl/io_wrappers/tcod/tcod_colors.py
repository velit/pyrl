from __future__ import annotations

from pyrl.types.glyphs import Color

color_map: dict[Color, tuple[int, int, int]] = {
    Color.Red:           (175, 0, 0),
    Color.Green:         (0, 175, 0),
    Color.Blue:          (0, 0, 175),
    Color.Purple:        (175, 0, 175),
    Color.Cyan:          (0, 175, 175),
    Color.Yellow:        (255, 255, 95),
    Color.Brown:         (150, 75, 0),
    Color.Dark_Blue:     (0, 0, 175),
    Color.Dark_Brown:    (135, 95, 0),
    Color.Light_Red:     (255, 95, 95),
    Color.Light_Green:   (95, 255, 95),
    Color.Light_Blue:    (95, 95, 255),
    Color.Light_Purple:  (255, 95, 255),
    Color.Light_Cyan:    (95, 255, 255),
    Color.White:         (255, 255, 255),
    Color.Light:         (218, 218, 218),
    Color.Normal:        (187, 187, 187),
    Color.Light_Gray:    (168, 168, 168),
    Color.Gray:          (138, 138, 138),
    Color.Dark_Gray:     (108, 108, 108),
    Color.Dark:          (78, 78, 78),
    Color.Darker:        (48, 48, 48),
    Color.Darkest:       (20, 20, 20),
    Color.Black:         (0, 0, 0),
}
