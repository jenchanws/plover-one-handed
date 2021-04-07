from plover.system.english_stenotype import *

KEYS = (
  ('#', 'l', 'r')  # l = left only, r = right only
  + KEYS[1:]  # All but '#'
)

KEYMAPS = {
  'Keyboard': {
    '-F': '1',
    '-R': 'q',
    '-P': '2',
    '-B': 'w',
    '-L': '3',
    '-G': 'e',
    '-T': '4',
    '-S': 'r',
    '-D': '5',
    '-Z': 't',
    '#': 'f',
    'A-': 'y',
    'O-': 'h',
    '-E': 'b',
    '-U': 'g',
    'l': 'n',
    'r': 'm',
    'arpeggiate': 'space',
    'no-op': ('a', 's', 'd'),
  }
}
