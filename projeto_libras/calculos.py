import os


def str2float(list_):
    for i, value in enumerate(list_):
        list_[i] = float(list_[i])
    return list_


def verify_hand_direction(hand):
    """
    Verifica se mão está voltada para cima (up) ou para baixo (down).
    Para isso são verifica-se os valores das pontas dos dedos e compara-se com o valor do pulso.
    """

    # Ponta dos dedos (valor da vertical, y)
    pos_thumb = hand.landmark[4].y  # Polegar
    pos_index_finger = hand.landmark[8].y  # Indicador
    pos_middle_finger = hand.landmark[12].y  # Médio
    pos_ring_finger = hand.landmark[16].y  # Anelar
    pos_pinky = hand.landmark[20].y  # Mínimo

    # Lista dos valores das pontas dos dedos
    fingers = [pos_thumb, pos_index_finger, pos_middle_finger, pos_ring_finger, pos_pinky]

    # Posicao do pulso (referência)
    pos_wrist = hand.landmark[0].y  # Pulso

    # Obs.: ponto (0,0) é o campo superior esquerda da imagem
    # Se todas as pontas do dedos tiverem valor superior ao valor do pulso, mão está para 'baixo',
    # caso contrário, está para 'cima'

    aux = 0  # Variável auxiliar
    for elem in fingers:
        # print(elem, pos_wrist)
        if elem < pos_wrist:
            aux += 1
    # print(aux)

    if aux == 5:  # Todos as pontas dos dedos estão acima do pulso
        return "up"
    else:
        return "down"

