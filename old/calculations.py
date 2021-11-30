from copy import deepcopy

# --- Variáveis globais ---
# Dedos
HAND_FINGERS = ["thumb", "index-finger", "middle-finger", "ring-finger", "pinky"]

# Parâmetros utilizados nos cálculos
DIFF_VALUE = 20  # Utilizado para determinar se dedo está esticado ou dobrado
DIFF_VALUE_2 = 49  # Utilizado para determinar se dedos adjancente está próximo ou não
# -------------------------


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


def extract_finger_points(hand, img_height, img_width):
    """
    Cria um dicionário os valores dos pontos dos dedos dão mão. Cada dedo é compostos por 4 pontos.
    :param hand:
    :param img_height: altura da imagem
    :param img_width: largura da imagem
    :return: dicionário com os valores dos pontos em pixel
    """
    hand_fingers_points = dict()

    for finger in HAND_FINGERS:
        if finger == "thumb":  # Vim da referência
            init = 1
        elif finger == "index-finger":
            init = 5
        elif finger == "middle-finger":
            init = 9
        elif finger == "ring-finger":
            init = 13
        elif finger == "pinky":
            init = 17
        else:
            raise Exception("Dedo não encontrado")

        # Pontos do dedo
        # -> 0: base do dedo
        # -> 3: ponta do dedo
        points_x = []
        points_y = []
        points_z = []  # TODO: adicionar tb ?
        len_finger = 4  # Número de pontos de um dedo

        for i in range(init, init + len_finger):
            points_x.append(hand.landmark[i].x * img_width)
            points_y.append(hand.landmark[i].y * img_height)

        # Atualiza dicionário
        points = {'x': points_x, 'y': points_y}
        hand_fingers_points.update({finger: points})

    return hand_fingers_points


def verify_hand_finger_condition(finger, points_y, hand_direction):
    """

    :param finger:
    :param points_y:
    :param hand_direction:
    :return:
    """

    # TODO: melhorar função deixar estado "esticado" mais bem explicado ? Ideia:
    #  explicitar melhor os estados (esticado na vertical, esticado na horizontal) e
    #  utilizar uma função para calcular o ângulo dos dedos

    # TODO: normalizar valor!!!!!!!!!!

    # Caso mão voltada para cima
    if hand_direction == "up":

        # Caso dedo for polegar
        if finger == "thumb":

            if points_y[3] > points_y[2]:  # Ponta do dedo (3) com valor maior que base do dedo (1)
                state = "bent"  # Dobrado
            else:
                if points_y[2] - points_y[3] < DIFF_VALUE:
                    state = "bent"  # Dobrado
                else:
                    state = "stretched"  # Esticado

        # Caso outros dedos
        else:

            # Ponta do dedo (3) com valor maior que base do dedo (1)
            if points_y[3] > points_y[1]:
                state = "bent"  # Dobrado
            else:
                state = "stretched"  # Esticado

    # Caso mão voltada para baixo ("down")
    else:

        # Caso dedo for polegar
        if finger == "thumb":

            if points_y[2] > points_y[3]:  # Ponta do dedo (3) com valor menor que base do dedo (1)
                state = "bent"  # Dobrado
            else:
                if points_y[3] - points_y[2] < DIFF_VALUE:
                    state = "bent"  # Dobrado
                else:
                    state = "stretched"  # Esticado

        # Caso outros dedos
        else:

            # Ponta do dedo (3) com valor menor que base do dedo (1)
            if points_y[3] < points_y[1]:
                state = "bent"  # Dobrado
            else:
                state = "stretched"  # Esticado

    return state


def compute_distance_adjacent_finger(finger_name, adjacent_finger, hand_fingers_points):
    # Distãncia entre ponta dos dedos
    finger_distance = abs(hand_fingers_points[adjacent_finger]['x'][3] - hand_fingers_points[finger_name]['x'][3])

    # Dividir por um valor padrão para valor não ser afetado por mão próxima ou distante na imagem
    reference_distance = abs(hand_fingers_points['index-finger']['y'][0] - hand_fingers_points['index-finger']['y'][3])

    # Cálculo
    distance = finger_distance/reference_distance*100

    return distance


def verify_adjacent_finger(states_, finger_name, adjacent_finger, hand_fingers_points):

    # Dividir por um valor padrão para valor não ser afetado por mão próxima ou distante na imagem
    reference_distance = abs(hand_fingers_points['index-finger']['y'][0] - hand_fingers_points['index-finger']['y'][3])

    # Compara se os dedos têm o mesmo estado ("esticado" ou "dobrado")
    if states_[finger_name] == states_[adjacent_finger]:

        if finger_name in ['thumb']:  # TODO: verificar caso para o polegar !!!

            # TODO: fazer
            # Distãncia entre ponta dos dedos
            finger_distance = abs(hand_fingers_points[adjacent_finger]['x'][3] - hand_fingers_points[finger_name]['x'][3])

        else:

            # Distãncia entre ponta dos dedos
            finger_distance = abs(hand_fingers_points[adjacent_finger]['x'][3] - hand_fingers_points[finger_name]['x'][3])

        # Cálculo
        distance = finger_distance/reference_distance*100

        if distance < DIFF_VALUE_2:
            # Próximo do dedo adjacente
            state_adjacent_finger = f"next to {adjacent_finger}"
        else:
            # Distante do dedo adjacente
            state_adjacent_finger = f"away from {adjacent_finger}"

    # Estados diferentes
    else:
        # Distante do dedo adjacente
        state_adjacent_finger = f"away from {adjacent_finger}"

    # Lista de características: condição do dedo e estado com relação ao dedo adjacente
    state_list = [states_[finger_name], state_adjacent_finger]

    return state_list


def verify_hand_fingers_states(hand, img_height, hand_direction, hand_fingers_points):
    """

    :param hand:
    :param img_height:
    :param hand_direction:
    :param hand_fingers_points:
    :return:
    """

    finger_states = dict()
    # Obs.: ponto (0,0) é o canto superior esquerdo da imagem

    for finger in HAND_FINGERS:
        # Pontos do dedo
        points_y = hand_fingers_points[finger]['y']

        # 1. Verifica estado do dedo (esticado ou dobrado)
        state = verify_hand_finger_condition(finger=finger, points_y=points_y, hand_direction=hand_direction)  # TODO: melhorar e aprimorar função

        # Atualiza dicionário com estado de cada dedo
        finger_states.update({finger: state})

    finger_states_copy = deepcopy(finger_states)  # Cria uma cópia dos estados

    for i, finger in enumerate(HAND_FINGERS):
        # Último dedo (mínimo)
        if i == len(HAND_FINGERS) - 1:
            adjacent_finger = HAND_FINGERS[len(HAND_FINGERS)-2]  # Anelar
        else:
            adjacent_finger = HAND_FINGERS[i+1]

        # 2. Verifica distância do dedo com relação ao seu adjacente
        state_list = verify_adjacent_finger(states_=finger_states_copy, finger_name=finger,
                                            adjacent_finger=adjacent_finger, hand_fingers_points=hand_fingers_points)  # TODO: terminar função

        # Atualiza dicionário com uma lista: o estado de cada dedo e se está próximo ou não do dedo adjacente
        finger_states.update({finger: state_list})

    return finger_states

