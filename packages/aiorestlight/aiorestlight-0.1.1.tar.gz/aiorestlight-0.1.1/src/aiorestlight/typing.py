from typing import TypedDict

class Pixel(TypedDict):
    """Pixel info"""

    red: int
    green: int
    blue: int

class PixelData(TypedDict):
    """Pixel Layout"""

    count: int
    values: list[Pixel]

class StateData(TypedDict):
    """Light state"""

    on: bool
    brightness: int
    hue: int
    saturation: int
    pixels: PixelData

class EffectsData(TypedDict):
    """Effects Data"""

    values: list[str]
    select: str
    
class InfoData(TypedDict):
    """REST API Info"""

    name: str
    model: str
    state: StateData
    effects: EffectsData