from enum import Enum

# --- Informações ----
# Alfabeto Manual de Libras:
#   - 26 letras
# Letras não identificáveis:
#   - 6 letras (H, J, K, X, Y, Z) pois envolvem movimento em sua execução
# Letras que se confundem:
#   - C e O
#   - S e E
#   - R e U
# Letras as quais a caracterização não foi muito boa:
#   - 9 letras: C, E, S, M, N, O, P, R, U
# Resumo:
#   - 26 letras do alfabeto manual de Libras
#   - 20 letras possíveis de identificar utilizando técnica abordada (estimativa de pose)
#   - 11 letras com detecção razoável
# --------------------


class AlphabetLetters(Enum):
    # Letra A - 1 dicionário
    A = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'next to index-finger'],
            'index-finger': ['bent', 'next to middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    # Letra B - 2 dicionários
    B = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
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
            'thumb': ['stretched', 'next to index-finger'],  # Observação: correto é o dicionário acima, polegar dobrado, trata-se de uma
            'index-finger': ['stretched', 'next to middle-finger'],  # limitação do autor que não consegue dobrar o polegar
            'middle-finger': ['stretched', 'next to ring-finger'],
            'ring-finger': ['stretched', 'next to pinky'],
            'pinky': ['stretched', 'next to ring-finger']
        }
    }
    # Letra C - 3 dicionários - caracterização de letra ruim # TODO: verificar
    C = {
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
    C__ = {
        'direction': 'up',
        'label': 'right',
        'side': 'side',
        'position': 'rotated',
        'fingers_states': {
            'thumb': ['bent', 'next to index-finger'],
            'index-finger': ['bent', 'next to middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    # Letra D - 2 dicionários
    D = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'far away from index-finger'],
            'index-finger': ['stretched', 'away from middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    D_ = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['bent', 'next to index-finger'],
            'index-finger': ['stretched', 'away from middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    # Letra E - 2 dicionários  # TODO: verificar
    E = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['bent', 'next to index-finger'],
            'index-finger': ['bent', 'next to middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    E_ = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['bent', 'away from index-finger'],
            'index-finger': ['bent', 'next to middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    # Letra F - 1 dicionário
    F = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'next to index-finger'],
            'index-finger': ['bent', 'away from middle-finger'],
            'middle-finger': ['stretched', 'next to ring-finger'],
            'ring-finger': ['stretched', 'next to pinky'],
            'pinky': ['stretched', 'next to ring-finger']
        }
    }
    # E_ = {
    #     'direction': 'up',
    #     'label': 'right',
    #     'side': 'front',
    #     'position': 'neutral',
    #     'fingers_states': {
    #         'thumb': ['bent', 'away to index-finger'],
    #         'index-finger': ['bent', 'next to middle-finger'],
    #         'middle-finger': ['bent', 'next to ring-finger'],
    #         'ring-finger': ['bent', 'next to pinky'],
    #         'pinky': ['bent', 'next to ring-finger']
    #     }
    # }
    # Letra G - 1 dicionário
    G = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'next to index-finger'],
            'index-finger': ['stretched', 'away from middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    # Letra I - 2 dicionários
    I = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'far away from index-finger'],
            'index-finger': ['bent', 'next to middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'away from pinky'],
            'pinky': ['stretched', 'away from ring-finger']
        }
    }
    I_ = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'next to index-finger'],
            'index-finger': ['bent', 'next to middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'away from pinky'],
            'pinky': ['stretched', 'away from ring-finger']
        }
    }
    # Letra L - 2 dicionários
    L = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['bent', 'away from index-finger'],
            'index-finger': ['stretched', 'away from middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    L_ = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['bent', 'far away from index-finger'],
            'index-finger': ['stretched', 'away from middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    # Letra M - 3 dicionários  # TODO: verificar
    M = {
        'direction': 'down',
        'label': 'right',
        'side': 'back',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['bent', 'next to index-finger'],
            'index-finger': ['stretched', 'next to middle-finger'],
            'middle-finger': ['stretched', 'next to ring-finger'],
            'ring-finger': ['stretched', 'next to pinky'],
            'pinky': ['stretched', 'next to ring-finger']  # Dificuldade de determinar estado de dedo oculto, polegar deveria ser considerado dobrado (bent)
        }
    }
    M_ = {
        'direction': 'down',
        'label': 'right',
        'side': 'back',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'next to index-finger'],
            'index-finger': ['stretched', 'next to middle-finger'],
            'middle-finger': ['stretched', 'next to ring-finger'],
            'ring-finger': ['stretched', 'next to pinky'],
            'pinky': ['stretched', 'next to ring-finger']  # Dificuldade de determinar estado de dedo oculto, polegar deveria ser considerado dobrado (bent)
        }
    }
    M__ = {
        'direction': 'down',
        'label': 'right',
        'side': 'back',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'next to index-finger'],
            'index-finger': ['stretched', 'next to middle-finger'],
            'middle-finger': ['stretched', 'next to ring-finger'],
            'ring-finger': ['stretched', 'away from pinky'],
            'pinky': ['bent', 'away from ring-finger']  # Dificuldade de determinar estado de dedo oculto
        }
    }
    # Letra N - 2 dicionários  # TODO: verificar
    N = {
        'direction': 'down',
        'label': 'right',
        'side': 'back',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'next to index-finger'],
            'index-finger': ['stretched', 'next to middle-finger'],
            'middle-finger': ['stretched', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']  # Dificuldade de determinar estado de dedo oculto
        }
    }
    N_ = {
        'direction': 'down',
        'label': 'right',
        'side': 'back',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'next to index-finger'],
            'index-finger': ['stretched', 'next to middle-finger'],
            'middle-finger': ['stretched', 'away from ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']  # Dificuldade de determinar estado de dedo oculto
        }
    }
    # Letra O - 2 dicionários  # TODO: verificar
    O = {
        'direction': 'up',
        'label': 'right',
        'side': 'side',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['bent', 'far away from index-finger'],
            'index-finger': ['bent', 'next to middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']  # Dificuldade de determinar estado de dedo oculto
        }
    }
    O_ = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'far away from index-finger'],
            'index-finger': ['bent', 'next to middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    # Letra P - 4 dicionários  # TODO: verificar
    P = {
        'direction': 'up',
        'label': 'right',
        'side': 'side',
        'position': 'rotated',
        'fingers_states': {
            'thumb': ['bent', 'next to index-finger'],
            'index-finger': ['stretched', 'away from middle-finger'],
            'middle-finger': ['stretched', 'away from ring-finger'],
            'ring-finger': ['stretched', 'next to pinky'],
            'pinky': ['stretched', 'next to ring-finger']
        }
    }
    P_ = {
        'direction': 'up',
        'label': 'right',
        'side': 'side',
        'position': 'rotated',
        'fingers_states': {
            'thumb': ['bent', 'next to index-finger'],
            'index-finger': ['stretched', 'away from middle-finger'],
            'middle-finger': ['stretched', 'away from ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    P__ = {
        'direction': 'up',
        'label': 'right',
        'side': 'side',
        'position': 'rotated',
        'fingers_states': {
            'thumb': ['bent', 'next to index-finger'],
            'index-finger': ['stretched', 'away from middle-finger'],
            'middle-finger': ['bent', 'away from ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['stretched', 'next to ring-finger']
        }
    }
    P___ = {
        'direction': 'up',
        'label': 'right',
        'side': 'side',
        'position': 'rotated',
        'fingers_states': {
            'thumb': ['stretched', 'next to index-finger'],
            'index-finger': ['stretched', 'away from middle-finger'],
            'middle-finger': ['bent', 'away from ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['stretched', 'next to ring-finger']
        }
    }
    # Letra Q - 1 dicionário
    Q = {
        'direction': 'down',
        'label': 'right',
        'side': 'back',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['bent', 'away from index-finger'],
            'index-finger': ['stretched', 'away from middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    # Letra R - 2 dicionários  # TODO: verificar
    R = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['bent', 'next to index-finger'],
            'index-finger': ['stretched', 'next to middle-finger'],
            'middle-finger': ['stretched', 'away from ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    R_ = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'far away from index-finger'],
            'index-finger': ['stretched', 'next to middle-finger'],
            'middle-finger': ['stretched', 'away from ring-finger'],
            'ring-finger': ['bent', 'away from pinky'],
            'pinky': ['bent', 'away from ring-finger']
        }
    }
    # Letra S - 2 dicionários  # TODO: verificar
    S = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['bent', 'far away from index-finger'],
            'index-finger': ['bent', 'next to middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    S_ = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['bent', 'next to index-finger'],
            'index-finger': ['bent', 'next to middle-finger'],
            'middle-finger': ['bent', 'next to ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    # S__ = {
    #     'direction': 'up',
    #     'label': 'right',
    #     'side': 'front',
    #     'position': 'neutral',
    #     'fingers_states': {
    #         'thumb': ['stretched', 'far away from index-finger'],
    #         'index-finger': ['bent', 'next to middle-finger'],
    #         'middle-finger': ['bent', 'next to ring-finger'],
    #         'ring-finger': ['bent', 'next to pinky'],
    #         'pinky': ['bent', 'next to ring-finger']
    #     }
    # }
    # Letra T
    # Letra T - 1 dicionário
    T = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'next to index-finger'],
            'index-finger': ['bent', 'away from middle-finger'],
            'middle-finger': ['stretched', 'away from ring-finger'],
            'ring-finger': ['stretched', 'away from pinky'],
            'pinky': ['stretched', 'away from ring-finger']
        }
    }
    # Letra U - 3 dicionários  # TODO: verificar
    U = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'away from index-finger'],
            'index-finger': ['stretched', 'next to middle-finger'],
            'middle-finger':  ['stretched', 'away from ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    U_ = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'next to index-finger'],
            'index-finger': ['stretched', 'next to middle-finger'],
            'middle-finger': ['stretched', 'away from ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    U__ = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['bent', 'away from index-finger'],
            'index-finger': ['stretched', 'next to middle-finger'],
            'middle-finger': ['stretched', 'away from ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    # Letra V - 3 dicionários
    V = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['bent', 'away from index-finger'],
            'index-finger': ['stretched', 'away from middle-finger'],
            'middle-finger': ['stretched', 'away from ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    # V_ = {
    #     'direction': 'up',
    #     'label': 'right',
    #     'side': 'front',
    #     'position': 'neutral',
    #     'fingers_states': {
    #         'thumb': ['bent', 'far away from index-finger'],
    #         'index-finger': ['stretched', 'far away from middle-finger'],
    #         'middle-finger': ['stretched', 'far away from ring-finger'],
    #         'ring-finger': ['bent', 'next to pinky'],
    #         'pinky': ['bent', 'next to ring-finger']
    #     }
    # }
    # V__ = {
    #     'direction': 'up',
    #     'label': 'right',
    #     'side': 'front',
    #     'position': 'neutral',
    #     'fingers_states': {
    #         'thumb': ['bent', 'away from index-finger'],
    #         'index-finger': ['stretched', 'away from middle-finger'],
    #         'middle-finger': ['stretched', 'far away from ring-finger'],
    #         'ring-finger': ['bent', 'next to pinky'],
    #         'pinky': ['bent', 'next to ring-finger']
    #     }
    # }
    V_ = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'next to index-finger'],
            'index-finger': ['stretched', 'away from middle-finger'],
            'middle-finger': ['stretched', 'away from ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    V__ = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['bent', 'next to index-finger'],
            'index-finger': ['stretched', 'away from middle-finger'],
            'middle-finger': ['stretched', 'away from ring-finger'],
            'ring-finger': ['bent', 'next to pinky'],
            'pinky': ['bent', 'next to ring-finger']
        }
    }
    # Letra W - 2 dicionários
    W = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['stretched', 'next to index-finger'],
            'index-finger': ['stretched', 'away from middle-finger'],
            'middle-finger': ['stretched', 'away from ring-finger'],
            'ring-finger': ['stretched', 'away from pinky'],
            'pinky': ['bent', 'away from ring-finger']
        }
    }
    W_ = {
        'direction': 'up',
        'label': 'right',
        'side': 'front',
        'position': 'neutral',
        'fingers_states': {
            'thumb': ['bent', 'next to index-finger'],
            'index-finger': ['stretched', 'away from middle-finger'],
            'middle-finger': ['stretched', 'away from ring-finger'],
            'ring-finger': ['stretched', 'away from pinky'],
            'pinky': ['bent', 'away from ring-finger']
        }
    }


def identify_letter(alphabet_letters, states):
    """
    Compara o estado de uma mão (e dedos) detectada e rastreada com estados pré-definidos
    que correspondem a letras do alfabeto manual de Libras.
    :param alphabet_letters: letras do alfabeto com suas características (dicionário)
    :param states: estado de uma mão detectada e seus dedos
    :return: letra indentifica ou vazio
    """
    for letter in alphabet_letters:
        if letter.value == states:
            return letter.name
    return ""
