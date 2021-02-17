#! /usr/bin/envy python3
"""Library to read and modify the playerPrefs file."""

from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import IO, Union


__all__ = ['Control', 'Color', 'Hat', 'Skin', 'Pet', 'Language', 'PlayerPrefs']


BOOL = {'True': True, 'False': False}


class U8(int):
    """A 8-bit unsigned int."""

    def __init__(self, value):
        if 0 <= int(value) <= 255:
            super().__init__()
        else:
            raise ValueError('UInt7 must be between 0 and 255.')


class Control(IntEnum):
    """Control settings."""

    MOUSE = 0
    MOUSE_AND_KEYBOARD = 1

    def __str__(self):
        return str(self.value)


class Color(IntEnum):
    """Available colors."""

    RED = 0
    BLUE = 1
    GREEN = 2
    PINK = 3
    ORANGE = 4
    YELLOW = 5
    BLACK = 6
    WHITE = 7
    PURPLE = 8
    BROWN = 9
    CYAN = 10
    LIME = 11

    def __str__(self):
        return str(self.value)


class Hat(IntEnum):
    """Available hats."""

    NONE = 0
    PARTY = 28
    FEDORA = 43
    SKI = 44
    SURGICAL_MASK = 47
    COWBOY = 49
    BANANA = 50
    BALACLAVA = 51
    MOUSE_EARS = 52
    CHEESE = 53
    CHERRY = 54
    FRIED_EGG = 55
    BLACK_HAT = 56
    FLAMINGO = 57
    FLOWER = 58
    ROMAN = 59
    LEAVES = 60
    CROWN = 30
    EYEBROWS = 31
    HALO = 32
    POINTED_HAT = 33
    DIVING_GOGGLES = 36
    STICKMAN = 37
    TELESCOPE_EYE = 40
    TOILET_PAPER = 41
    LEPRECHAUN = 42
    FLAT_CAP = 34
    PLUNGER = 35
    TOPEE = 38
    SHERRIFF = 39
    ANTENNA = 76
    ASTRONAUT = 1
    BALLOON = 77
    BASEBALL_CAP = 2
    NEST = 78
    NINJA_HEADBAND = 79
    ALIEN = 3
    BROWN_HAT = 4
    PILOT = 5
    WET_FLOOR_SIGN = 80
    CHEF = 81
    BLUE_HAT = 82
    BANDANA = 83
    DOUBLE_TOP_HAT = 6
    STICKY_NOTE = 84
    FEZ = 85
    FLOWER_POT = 7
    PILOT_GREEN = 86
    NIGHT_VISION = 8    # What is that?
    ELVIS = 87
    BUILDING_SITE = 9
    UNKNOWN = 88    # What is that?
    SOLDIER = 89
    OFFICER = 10
    MINIME = 90
    NINJA_MASK = 90
    PAPER = 11
    CLOWN = 12
    POLICE = 13
    HORNS = 92
    BOBBLE = 93
    SURGEON = 14
    TOPHAT = 15
    TOWEL = 16
    BEARSKIN = 17
    VIKING = 18
    SECURITY = 19
    WHITE_TOPHAT = 29

    def __str__(self):
        return str(self.value)


class Skin(IntEnum):
    """Available skins."""

    NONE = 0
    ASTRONAUT = 1
    PILOT = 2
    BLUEY = 3
    SOLDIER = 4
    POLICE = 5
    LAB_COAT = 6
    SUIT_BLACK = 7
    SUIT_WHITE = 8
    SECURITY = 9

    def __str__(self):
        return str(self.value)


class Pet(IntEnum):
    """Available pets."""

    NONE = 0

    def __str__(self):
        return str(self.value)


class Language(IntEnum):
    """Available languages."""

    ENGLISH = 0
    SPANISH = 1
    PORTOGUESE = 2
    KOREAN = 3
    RUSSIAN = 4

    def __str__(self):
        return str(self.value)


@dataclass
class PlayerPrefs:  # pylint: disable=R0902
    """Among Us player preferences."""

    name: str
    control: Control
    color: Color
    unknown3: int
    unknown4: bool
    unknown5: bool
    unknown6: bool
    unknown7: int
    unknown8: bool
    unknown9: bool
    hat: Hat
    sfx: U8
    music: U8
    unknown13: int
    unknown14: int
    skin: Skin
    pet: Pet
    censor_chat: bool
    language: Language
    vsync: bool
    unknown20: int
    unknown21: int

    def __iter__(self):
        yield self.name
        yield self.control
        yield self.color
        yield self.unknown3
        yield self.unknown4
        yield self.unknown5
        yield self.unknown6
        yield self.unknown7
        yield self.unknown8
        yield self.unknown9
        yield self.hat
        yield self.sfx
        yield self.music
        yield self.unknown13
        yield self.unknown14
        yield self.skin
        yield self.pet
        yield self.censor_chat
        yield self.language
        yield self.vsync
        yield self.unknown20
        yield self.unknown21

    def __str__(self):
        return ','.join(map(str, self))

    @classmethod
    def from_list(cls, lst: list[str]) -> PlayerPrefs:
        """Reads the player preferences from an iterable str."""
        if len(lst) != 22:
            raise ValueError('Excpected iterable with 22 fields.')

        return cls(lst[0], Control(int(lst[1])), Color(int(lst[2])),
                   int(lst[3]), BOOL[lst[4]], BOOL[lst[5]], BOOL[lst[6]],
                   int(lst[7]), BOOL[lst[8]], BOOL[lst[9]], Hat(int(lst[10])),
                   U8(lst[11]), U8(lst[12]), int(lst[13]), int(lst[14]),
                   Skin(int(lst[15])), Pet(int(lst[16])), BOOL[lst[17]],
                   Language(int(lst[18])), BOOL[lst[19]], int(lst[20]),
                   int(lst[21]))

    @classmethod
    def from_string(cls, string: str) -> PlayerPrefs:
        """Reads the player preferences from a string."""
        return cls.from_list(string.split(','))

    @classmethod
    def from_buffer(cls, buf: IO) -> PlayerPrefs:
        """Reads the player preferences from a file-like object."""
        return cls.from_string(buf.read())

    @classmethod
    def from_path(cls, path: Union[Path, str]) -> PlayerPrefs:
        """Reads the player preferences from the given file."""
        with open(path, 'r') as file:
            return cls.from_buffer(file)

    def write(self, path: Union[Path, str]) -> None:
        """Writes the player preferences to the given file."""
        with open(path, 'w') as file:
            file.write(str(self))


def test():
    """Tests the reader."""

    steamapps = Path.home() / '.local/share/Steam/steamapps'
    drive_c = steamapps / 'compatdata/945360/pfx/drive_c'
    appdata_ll = drive_c.joinpath / 'users/steamuser/AppData/LocalLow'
    amongus = appdata_ll / 'Innersloth/Among Us/playerPrefs'
    player_prefs = PlayerPrefs.from_path(amongus)
    print(repr(player_prefs))


if __name__ == '__main__':
    test()
