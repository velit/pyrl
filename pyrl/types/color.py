from __future__ import annotations

from enum import Enum

class Color(Enum):
    Red          = "Red"
    Green        = "Green"
    Blue         = "Blue"

    Purple       = "Purple"
    Cyan         = "Cyan"
    Yellow       = "Yellow"
    Brown        = "Brown"

    Dark_Blue    = "Dark Blue"
    Dark_Brown   = "Dark Brown"

    Light_Red    = "Light Red"
    Light_Green  = "Light Green"
    Light_Blue   = "Light Blue"

    Light_Purple = "Light Purple"
    Light_Cyan   = "Light Cyan"

    White        = "White"       # Brightness 255
    Light        = "Light"       # 218
    Normal       = "Normal"      # 187
    Light_Gray   = "Light Gray"  # 168
    Gray         = "Gray"        # 138
    Dark_Gray    = "Dark Gray"   # 108
    Dark         = "Dark"        # 78
    Darker       = "Darker"      # 48
    Darkest      = "Darkest"     # 18
    Black        = "Black"       # 0

    def __str__(self) -> str:
        return self.value

ColorPair = tuple[Color, Color]

class ColorPairs:
    Red:          ColorPair = (Color.Red,          Color.Black)
    Green:        ColorPair = (Color.Green,        Color.Black)
    Blue:         ColorPair = (Color.Blue,         Color.Black)
    Purple:       ColorPair = (Color.Purple,       Color.Black)
    Cyan:         ColorPair = (Color.Cyan,         Color.Black)
    Yellow:       ColorPair = (Color.Yellow,       Color.Black)
    Brown:        ColorPair = (Color.Brown,        Color.Black)
    Dark_Blue:    ColorPair = (Color.Dark_Blue,    Color.Black)
    Dark_Brown:   ColorPair = (Color.Dark_Brown,   Color.Black)
    Light_Red:    ColorPair = (Color.Light_Red,    Color.Black)
    Light_Green:  ColorPair = (Color.Light_Green,  Color.Black)
    Light_Blue:   ColorPair = (Color.Light_Blue,   Color.Black)
    Light_Purple: ColorPair = (Color.Light_Purple, Color.Black)
    Light_Cyan:   ColorPair = (Color.Light_Cyan,   Color.Black)
    White:        ColorPair = (Color.White,        Color.Black)
    Light:        ColorPair = (Color.Light,        Color.Black)
    Normal:       ColorPair = (Color.Normal,       Color.Black)
    Light_Gray:   ColorPair = (Color.Light_Gray,   Color.Black)
    Gray:         ColorPair = (Color.Gray,         Color.Black)
    Dark_Gray:    ColorPair = (Color.Dark_Gray,    Color.Black)
    Dark:         ColorPair = (Color.Dark,         Color.Black)
    Darker:       ColorPair = (Color.Darker,       Color.Black)
    Darkest:      ColorPair = (Color.Darkest,      Color.Black)
    Black:        ColorPair = (Color.Black,        Color.Black)
    Cursor:       ColorPair = (Color.Black,        Color.Green)
