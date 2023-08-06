from itertools import product

from .colors import (
    BLACK,
    BLUE,
    COLOR_DICT,
    DARK_GREEN,
    DARK_RED,
    DEEP_BLUE,
    DEEP_CYAN,
    DEEP_GREEN,
    DEEP_GREY,
    DEEP_ORANGE,
    DEEP_RED,
    DEEP_VIOLET,
    DEEP_YELLOW,
    LIGHT_BLUE,
    LIGHT_GREEN,
    LIGHT_GREY,
    LIGHT_RED,
    WHITE,
)
from .utils import _register_blended_cmap, _register_listed_cmap

####################################################################################################
# DISCRETE COLORMAPS
####################################################################################################

standard_colors = [
    BLUE,
    LIGHT_GREY,
    LIGHT_BLUE,
    DEEP_GREY,
    DARK_RED,
    LIGHT_GREEN,
    LIGHT_RED,
    DARK_GREEN,
]
standard_cmap = _register_listed_cmap(standard_colors, "stwx:standard")

alternative_colors = [
    BLUE,
    LIGHT_GREY,
    DARK_RED,
    LIGHT_GREEN,
    LIGHT_BLUE,
    DEEP_GREY,
    LIGHT_RED,
    DARK_GREEN,
]
alternative_cmap = _register_listed_cmap(alternative_colors, "stwx:alternative")


deep_colors = [
    DEEP_BLUE,
    DEEP_RED,
    DEEP_GREEN,
    DEEP_VIOLET,
    DEEP_CYAN,
    DEEP_ORANGE,
]
deep_cmap = _register_listed_cmap(deep_colors, "stwx:deep")

####################################################################################################
# BLENDED COLORMAPS
####################################################################################################

bad2good_colors = [DARK_RED, DEEP_YELLOW, DARK_GREEN]
bad2good_cmap = _register_blended_cmap(bad2good_colors, "stwx:bad2good")

good2bad_colors = [DARK_GREEN, DEEP_YELLOW, DARK_RED]
good2bad_cmap = _register_blended_cmap(good2bad_colors, "stwx:good2bad")

for (name1, color1), (name2, color2) in product(COLOR_DICT.items(), COLOR_DICT.items()):
    cmap_colors_ = [color1, WHITE, color2]
    cmap_name_ = f"stwx:{name1}{name2}_diverging"
    _register_blended_cmap(cmap_colors_, cmap_name_)

for (name1, color1), (name2, color2) in product(COLOR_DICT.items(), COLOR_DICT.items()):
    if name1 != name2:
        cmap_colors_ = [color1, color2]
        cmap_name_ = f"stwx:{name1}{name2}_blend"
        _register_blended_cmap(cmap_colors_, cmap_name_)

for name, color in COLOR_DICT.items():
    cmap_colors_ = [color, WHITE]
    cmap_name_ = f"stwx:{name}_fade"
    _register_blended_cmap(cmap_colors_, cmap_name_)

for name, color in COLOR_DICT.items():
    cmap_colors_ = [BLACK, color, WHITE]
    cmap_name_ = f"stwx:{name}_rise"
    _register_blended_cmap(cmap_colors_, cmap_name_)
