from enum import Enum


class AlphabetLetters(Enum):
    A = {  # TODO: fazer
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            # 'thumb': ['stretched', 'away from index-finger'],
            # 'index-finger': ['bent', 'away from middle-finger'],
            # 'middle-finger': ['bent', 'away from ring-finger'],
            # 'ring-finger': ['bent', 'away from pinky'],
            # 'pinky': ['bent', 'away from ring-finger']
            'thumb': ['stretched', 'next to index-finger'],
            'index-finger': ['bent', 'next to middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    B = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            # 'thumb': ['stretched', 'next to index-finger'],
            'thumb': ['bent', 'next to index-finger'],
            'index-finger': ['stretched', 'next to middle-finger'],
            'middle-finger': ['stretched', 'next to ring-finger'],
            'ring-finger': ['stretched', 'next to pinky'],
            'pinky': ['stretched', 'next to ring-finger']
        }
    }
    B_ = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'next to index-finger'],
            'index-finger': ['stretched', 'next to middle-finger'],
            'middle-finger': ['stretched', 'next to ring-finger'],
            'ring-finger': ['stretched', 'next to pinky'],
            'pinky': ['stretched', 'next to ring-finger']
        }
    }
    C = {  # TODO: fazer
        'direction': 'up',
        'label': 'right',
        'side': 'side',
        'position': 'rotated',
        'fingers_states': {
            'thumb': ['bent', 'away from index-finger'],
            'index-finger': ['bent', 'next to middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    C_ = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'rotated',
        'fingers_states': {
            'thumb': ['bent', 'away from index-finger'],
            'index-finger': ['bent', 'next to middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    # C__ = {  # TODO: identificar mais opções
    #     'direction': 'up',
    #     'label': 'right',
    #     'side': 'front',
    #     'position': 'rotated',
    #     'fingers_states': {
    #         'thumb': ['stretched', 'away from index-finger'],
    #         'index-finger': ['bent', 'next to middle-finger'],
    #         'middle-finger': ['bent', 'next to ring-finger'],
    #         'ring-finger': ['bent', 'next to pinky'],
    #         'pinky': ['bent', 'next to ring-finger']
    #     }
    # }


def identify_letter(alphabet_letters, states):
    for letter in alphabet_letters:
        if letter.value == states:
            return letter.name
    return ""
