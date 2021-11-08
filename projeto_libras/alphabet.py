from enum import Enum


class AlphabetLetters(Enum):
    A = {  # TODO: fazer
        'direction': 'up',
        'label': 'right',
        'fingers_states': {
            'thumb': ['stretched', 'away from index-finger'],  # TODO: verificar!
            'index-finger': ['bent', 'away from middle-finger'],
            'middle-finger': ['bent', 'away from ring-finger'],
            'ring-finger': ['bent', 'away from pinky'],
            'pinky': ['bent', 'away from ring-finger']
        }
    }
    B = {  # TODO: fazer
        'direction': 'up',
        'label': 'right',
        'fingers_states': {
            'thumb': ['stretched', 'next to index-finger'],   # TODO: verificar!
            'index-finger': ['stretched', 'next to middle-finger'],
            'middle-finger': ['stretched', 'next to ring-finger'],
            'ring-finger': ['stretched', 'next to pinky'],
            'pinky': ['stretched', 'next to ring-finger']
        }
    }
    C = {  # TODO: fazer
        'direction': 'up',
        'label': 'right',
        'fingers_states': {
            'thumb': ['bent', 'away from index-finger'],
            'index-finger': ['bent', 'away from middle-finger'],
            'middle-finger': ['bent', 'away from ring-finger'],
            'ring-finger': ['bent', 'away from pinky'],
            'pinky': ['bent', 'away from ring-finger']
        }
    }


def identify_letter(alphabet_letters, states):
    for letter in alphabet_letters:
        if letter.value == states:
            return letter.name
    return ""
