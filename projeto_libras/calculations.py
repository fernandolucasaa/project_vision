from copy import deepcopy
import math

# --- Variáveis globais ---
# Dedos
HAND_FINGERS = ["thumb", "index-finger", "middle-finger", "ring-finger", "pinky"]

# Parâmetros utilizados nos cálculos
THRESHOLD_THUMB_CONDITION = 80  # Utilizado para determinar se dedo está 'esticado' ou 'dobrado'

THRESHOLD_FINGER_DISTANCE = 150  # Utilizado para determinar se dedo esta 'próximo' ou 'afastado'
THRESHOLD_FINGER_DISTANCE_ = 200  # Utilizado para determinar se dedo está 'mais afastado'

THRESHOLD_THUMB_DISTANCE = 230  # Utilizado para determinar se dedo esta 'próximo' ou 'afastado'
THRESHOLD_THUMB_DISTANCE_ = 280  # Utilizado para determinar se dedo está 'mais afastado'

THRESHOLD_ANGLE = 30  # Utilizado para determinar se mão está em posição 'neutra' ou 'rotacionada'
# -------------------------


def str2float(list_):
    for i, value in enumerate(list_):
        list_[i] = float(list_[i])
    return list_


def verify_hand_direction(hand):
    """
    Verifica se mão (hand) está voltada para cima (up) ou para baixo (down).
    Para isso são verificados os valores das bases dos dedos (polegar, indicador, médio, anelar e mínimo)
    e compara-se com o valor do pulso, valores no eixo y.
    :param hand: mão detectada
    :return: direção da mão, para cima (up) ou para baixo (down)
    """

    # Base dos dedos (valor da vertical, y)
    pos_thumb = hand.landmark[1].y  # Polegar
    pos_index_finger = hand.landmark[5].y  # Indicador
    pos_middle_finger = hand.landmark[9].y  # Médio
    pos_ring_finger = hand.landmark[13].y  # Anelar
    pos_pinky = hand.landmark[17].y  # Mínimo

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

    if aux >= 4:  # Todos as pontas dos dedos estão acima do pulso
        hand_direction = "up"
    else:
        hand_direction = "down"
    return hand_direction


def verify_hand_side_foward(label, hand, hand_direction):
    """
    Verifica qual lado da mão está voltada para a câmera, se é a palma da mão (front) se é as costas da mesma (back)
    ou se a mão está de lado (side). Para isso são verificados os valores das bases dos dedos (polegar, indicador, médio,
    anelar e mínimo). Os valores são no eixo x.
    :param label: label da mão em questão (right ou left)
    :param hand: mão detectada
    :param hand_direction: direção da mão detectada
    :return: lado da mao voltado para a câmera
    """

    if label == "right":  # Caso mão direita

        if hand_direction == "up":
            # Base dos dedos (valor da vertical, y)
            pos_index_finger = hand.landmark[5].x  # Indicador
            pos_middle_finger = hand.landmark[9].x  # Médio
            pos_ring_finger = hand.landmark[13].x  # Anelar
            pos_pinky = hand.landmark[17].x  # Mínimo

            if pos_pinky > pos_ring_finger > pos_middle_finger > pos_index_finger:
                return "front"  # Palma da mão
            elif pos_pinky < pos_ring_finger < pos_middle_finger < pos_index_finger:
                return "back"  # Costas da mão
            else:
                return "side"  # Lado da mão

        elif hand_direction == "down":
            # Base dos dedos (valor da vertical, y)
            pos_index_finger = hand.landmark[5].x  # Indicador
            pos_middle_finger = hand.landmark[9].x  # Médio
            pos_ring_finger = hand.landmark[13].x  # Anelar
            pos_pinky = hand.landmark[17].x  # Mínimo

            if pos_pinky > pos_ring_finger > pos_middle_finger > pos_index_finger:
                return "back"  # Costas da mão
            elif pos_pinky < pos_ring_finger < pos_middle_finger < pos_index_finger:
                return "front"  # Palma da mão
            else:
                return "side"  # Lado da mão
        else:
            return ""

    elif label == "left":  # Caso mão esquerda

        if hand_direction == "up":
            # Base dos dedos (valor da vertical, y)
            pos_index_finger = hand.landmark[5].x  # Indicador
            pos_middle_finger = hand.landmark[9].x  # Médio
            pos_ring_finger = hand.landmark[13].x  # Anelar
            pos_pinky = hand.landmark[17].x  # Mínimo

            if pos_pinky > pos_ring_finger > pos_middle_finger > pos_index_finger:
                return "back"  # Costas da mão
            elif pos_pinky < pos_ring_finger < pos_middle_finger < pos_index_finger:
                return "front"  # Palma da mão
            else:
                return "side"  # Lado da mão

        elif hand_direction == "down":
            # Base dos dedos (valor da vertical, y)
            pos_index_finger = hand.landmark[5].x  # Indicador
            pos_middle_finger = hand.landmark[9].x  # Médio
            pos_ring_finger = hand.landmark[13].x  # Anelar
            pos_pinky = hand.landmark[17].x  # Mínimo

            if pos_pinky > pos_ring_finger > pos_middle_finger > pos_index_finger:
                return "front"  # Palma da mão
            elif pos_pinky < pos_ring_finger < pos_middle_finger < pos_index_finger:
                return "back"  # Costas da mão
            else:
                return "side"  # Lado da mão
        else:
            return ""
    else:
        return ""


def extract_finger_points(hand, img_height, img_width):
    """
    Cria um dicionário os valores dos pontos dos dedos dão mão. Cada dedo é compostos por 4 pontos.
    :param hand: mão detectada
    :param img_height: altura da imagem
    :param img_width: largura da imagem
    :return: dicionário com os valores dos pontos em pixel
    """
    hand_fingers_points = dict()

    for finger in HAND_FINGERS:
        if finger == "thumb":  # Verificar referência
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
        # 0: base do dedo, 3: ponta do dedo
        points_x = []
        points_y = []
        points_z = []
        len_finger = 4  # Número de pontos de um dedo

        for i in range(init, init + len_finger):
            points_x.append(hand.landmark[i].x * img_width)
            points_y.append(hand.landmark[i].y * img_height)
            points_z.append(hand.landmark[i].z * img_width)  # TODO: teste, verificar

        # Atualiza dicionário
        points = {'x': points_x, 'y': points_y, 'z': points_z}
        hand_fingers_points.update({finger: points})

    return hand_fingers_points


def verify_hand_finger_condition(finger, points_y, hand_direction, hand_fingers_points):
    """
    Verifica o estado, condição de um dedo em questão, ou seja, se está esticado (streched)
    ou dobrado (bent).
    :param finger: dedo analisado
    :param points_y: pontos no eixo y do dedo analisado
    :param hand_direction: direção da mão detectada
    :param hand_fingers_points: dicionário com as coordendas dos pontos dos dedos da mão
    :return: o estado do dedo analisado, esticado ou dobrado
    """

    # TODO:
    #  [melhoria]
    #  melhorar função para deixar estado "esticado" mais bem explicado ?
    #  Ideia: explicitar melhor os estados (esticado na vertical, esticado na horizontal, etc.) e
    #  utilizar uma função para calcular o ângulo dos dedos (!)

    # TODO:
    #  [limitação]
    #  não considera caso para mão de lado

    # Distância de referência (dimuir efeito da distância mão próxima ou distante da câmera)
    reference_distance = compute_reference_value(hand_fingers_points)

    # Caso mão voltada para cima
    if hand_direction == "up":
        # Caso dedo for polegar
        if finger == "thumb":
            if points_y[3] >= points_y[2]:  # Ponta do dedo (3) com valor maior que base do dedo (1)
                state = "bent"  # Dobrado
            else:
                diference = abs(points_y[2] - points_y[3])
                value = diference / reference_distance * 100
                # print(value)
                if value <= THRESHOLD_THUMB_CONDITION:  # Valor da constante: 80
                    state = "bent"  # Dobrado
                else:
                    state = "stretched"  # Esticado
        # Caso outros dedos
        else:
            # Ponta do dedo (3) com valor maior que base do dedo (1)
            if points_y[3] >= points_y[1]:
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
                diference = abs(points_y[2] - points_y[3])
                value = diference / reference_distance * 100
                # print(value)
                if value >= THRESHOLD_THUMB_CONDITION:  # Valor da constante: 80
                    state = "bent"  # Dobrado
                else:
                    state = "stretched"  # Esticado
        # Caso outros dedos
        else:
            # Ponta do dedo (3) com valor menor que base do dedo (1)
            if points_y[3] <= points_y[1]:
                state = "bent"  # Dobrado
            else:
                state = "stretched"  # Esticado

    return state


def compute_reference_value(hand_fingers_points):
    """
    Calcula a distância entre a base do dedo indicador e do dedo médio. Calcula distância
    em 3 dimensões.
    :param hand_fingers_points: dicionário com as coordendas dos pontos dos dedos da mão
    :return: distância entre a base do dedo indicador e do dedo médio
    """

    # Distância entre a base de dois dedos
    diff_y = hand_fingers_points['index-finger']['y'][0] - hand_fingers_points['middle-finger']['y'][0]
    diff_x = hand_fingers_points['index-finger']['x'][0] - hand_fingers_points['middle-finger']['x'][0]
    len_ = math.sqrt(pow(diff_x, 2) + pow(diff_y, 2))

    diff_z = hand_fingers_points['index-finger']['z'][0] - hand_fingers_points['middle-finger']['z'][0]
    length = math.sqrt(pow(len_, 2) + pow(diff_z, 2))

    return length


# def compute_thumb_diference(hand_fingers_points):
#     # Distância de referência (dimuir efeito da distância mão próxima ou distante da câmera)
#     reference_distance = compute_reference_value(hand_fingers_points)
#
#     points_y = hand_fingers_points['thumb']['y']
#
#     diference = abs(points_y[2] - points_y[3])
#     value = diference / reference_distance * 100
#
#     return value


def compute_distance_adjacent_finger(finger_name, adjacent_finger, hand_fingers_points):
    """
    Cálcula a distância entre a ponta do dedo analisado e a ponta do dedo adjacente. Divide
    por fator de correção (distância de referência).
    :param finger_name: dedo analisado
    :param adjacent_finger: dedo adjacente
    :param hand_fingers_points: dicionário com as coordendas dos pontos dos dedos da mão
    :return: distância entre os pontos dos dedos
    """

    # Distância de referência (diminuir efeito da distância mão próxima ou distante da câmera)
    reference_distance = compute_reference_value(hand_fingers_points)
    length = reference_distance

    # Distãncia entre ponta dos dedos
    finger_distance = compute_distance_between_points(x1=hand_fingers_points[adjacent_finger]['x'][3],
                                                      y1=hand_fingers_points[adjacent_finger]['y'][3],
                                                      z1=hand_fingers_points[adjacent_finger]['z'][3],
                                                      x2=hand_fingers_points[finger_name]['x'][3],
                                                      y2=hand_fingers_points[finger_name]['y'][3],
                                                      z2=hand_fingers_points[finger_name]['z'][3],
                                                      )
    # print(finger_distance)

    # Cálculo
    distance = finger_distance / length * 100

    return distance


def compute_distance_adjancent_finger_thumb(hand_fingers_points):
    """
    Cálcula a distância entre a base do dedo indicador e a ponta do dedo polegar. Divide
    por fator de correção (distância de referência).
    :param hand_fingers_points: dicionário com as coordendas dos pontos dos dedos da mão
    :return: distância entre os pontos dos dedos
    """

    # Distância de referência (diminuir efeito da distância mão próxima ou distante da câmera)
    reference_distance = compute_reference_value(hand_fingers_points)

    # Distância entre ponta do polegar e base do dedo indicador
    finger_distance = compute_distance_between_points(x1=hand_fingers_points['index-finger']['x'][0],
                                                      y1=hand_fingers_points['index-finger']['y'][0],
                                                      z1=hand_fingers_points['index-finger']['z'][0],
                                                      x2=hand_fingers_points['thumb']['x'][2],
                                                      y2=hand_fingers_points['thumb']['y'][2],
                                                      z2=hand_fingers_points['thumb']['z'][2],
                                                      )
    # Cálculo
    distance = finger_distance / reference_distance * 100

    return distance


def compute_distance_between_points(x1, y1, z1, x2, y2, z2):
    """
    Calcula a distância entre dois pontos, onde são passados por referência
    suas coordenadas em três dimensões.
    :param x1: valor no eixo x do ponto 1
    :param y1: valor no eixo y do ponto 1
    :param z1: valor no eixo z do ponto 1
    :param x2: valor no eixo x do ponto 2
    :param y2: valor no eixo y do ponto 2
    :param z2: valor no eixo z do ponto 2
    :return: distância em um espaço tridimensional entre dois pontos
    """
    diff_y = y1 - y2
    diff_x = x1 - x2
    len_ = math.sqrt(pow(diff_x, 2) + pow(diff_y, 2))

    diff_z = z1 - z2
    length = math.sqrt(pow(len_, 2) + pow(diff_z, 2))

    return length


def verify_adjacent_finger(states_, finger_name, adjacent_finger, hand_fingers_points):
    """
    Verifica se o dedo em questao está próximo ou afastado de seu dedo adjacente.
    :param states_: estado dos dedos da mão (dobrados ou esticados)
    :param finger_name: dedo analisado
    :param adjacent_finger: dedo adjacente ao dedo analisado
    :param hand_fingers_points: dicionário com as coordendas dos pontos dos dedos da mão
    :return: lista com as características do dedo analisado: se está dobrado ou esticado (passado por parâmetro)
    e se está próximo ou afastado de seu dedo adjacente
    """

    # Distância de referência (diminuir efeito da distância mão próxima ou distante da câmera)
    reference_distance = compute_reference_value(hand_fingers_points)

    if finger_name in ['thumb']:  # Polegar
        # Distância entre ponta do polegar e base do dedo indicador
        thumb_distance = compute_distance_adjancent_finger_thumb(hand_fingers_points=hand_fingers_points)

        # Cálculo
        distance = thumb_distance

        # Condição
        if distance <= THRESHOLD_THUMB_DISTANCE:
            # Próximo do dedo adjacente
            state_adjacent_finger = f"next to {adjacent_finger}"
        elif THRESHOLD_THUMB_DISTANCE < distance <= THRESHOLD_THUMB_DISTANCE_:
            # Afastado do dedo adjacente
            state_adjacent_finger = f"away from {adjacent_finger}"
        else:
            # Mais afastado do dedo adjacente
            state_adjacent_finger = f"far away from {adjacent_finger}"  # TODO: verificar se continua assim com três estados
    else:
        # Distãncia entre ponta dos dedos
        if finger_name in ['ring-finger']:
            finger_distance = compute_distance_between_points(x1=hand_fingers_points[adjacent_finger]['x'][3],
                                                              y1=hand_fingers_points[adjacent_finger]['y'][3],
                                                              z1=hand_fingers_points[adjacent_finger]['z'][3],
                                                              x2=hand_fingers_points[finger_name]['x'][2],
                                                              y2=hand_fingers_points[finger_name]['y'][2],
                                                              z2=hand_fingers_points[finger_name]['z'][2],
                                                              )
        elif finger_name in ['pinky']:
            finger_distance = compute_distance_between_points(x1=hand_fingers_points[adjacent_finger]['x'][2],
                                                              y1=hand_fingers_points[adjacent_finger]['y'][2],
                                                              z1=hand_fingers_points[adjacent_finger]['z'][2],
                                                              x2=hand_fingers_points[finger_name]['x'][3],
                                                              y2=hand_fingers_points[finger_name]['y'][3],
                                                              z2=hand_fingers_points[finger_name]['z'][3],
                                                              )
        else:  # index-finger, middle-finger
            finger_distance = compute_distance_between_points(x1=hand_fingers_points[adjacent_finger]['x'][3],
                                                              y1=hand_fingers_points[adjacent_finger]['y'][3],
                                                              z1=hand_fingers_points[adjacent_finger]['z'][3],
                                                              x2=hand_fingers_points[finger_name]['x'][3],
                                                              y2=hand_fingers_points[finger_name]['y'][3],
                                                              z2=hand_fingers_points[finger_name]['z'][3],
                                                              )
        # Cálculo
        distance = finger_distance / reference_distance * 100

        # Condição
        if distance <= THRESHOLD_FINGER_DISTANCE:
            # Próximo do dedo adjacente
            state_adjacent_finger = f"next to {adjacent_finger}"
        elif THRESHOLD_FINGER_DISTANCE < distance <= THRESHOLD_FINGER_DISTANCE_:
            # Afastado do dedo adjacente
            state_adjacent_finger = f"away from {adjacent_finger}"
        else:
            # Mais afastado do dedo adjacente
            state_adjacent_finger = f"far away from {adjacent_finger}"   # TODO: verificar se continua assim com três estados

    # # Estados diferentes
    # else:
    #     # Distante do dedo adjacente
    #     state_adjacent_finger = f"away from {adjacent_finger}"

    # Lista de características: condição do dedo (dobrado ou esticado) e estado com relação ao dedo adjacente (próximo ou distante)
    state_list = [states_[finger_name], state_adjacent_finger]

    return state_list


def verify_hand_fingers_states(hand_direction, hand_fingers_points):
    """
    Verifica o estado de cada dedo da mão. São determinados duas características: a condição do dedo em questão, ou seja,
    se está dobrado ou esticado; e se o dedo adjacente está próximo ou afastado.
    :param hand_direction: direção da mão detectada
    :param hand_fingers_points: dicionário com as coordenadas dos pontos de cada dedo da mão
    :return: dicionário com essas duas características de cada dedo da mão
    """

    finger_states = dict()
    # Obs.: ponto (0,0) é o canto superior esquerdo da imagem

    for finger in HAND_FINGERS:
        # Pontos do dedo. Coordenadas no eixo y
        points_y = hand_fingers_points[finger]['y']

        # 1. Verifica estado do dedo (esticado ou dobrado)
        state = verify_hand_finger_condition(finger=finger, points_y=points_y, hand_direction=hand_direction, hand_fingers_points=hand_fingers_points)  # TODO: acompanhar melhorias implementadas

        # Atualiza dicionário com estado de cada dedo
        finger_states.update({finger: state})

    finger_states_copy = deepcopy(finger_states)  # Cria uma cópia dos estados

    for i, finger in enumerate(HAND_FINGERS):
        # Último dedo (mínimo)
        if i == len(HAND_FINGERS) - 1:
            adjacent_finger = HAND_FINGERS[len(HAND_FINGERS) - 2]  # Anelar
        else:
            adjacent_finger = HAND_FINGERS[i + 1]

        # 2. Verifica distância do dedo com relação ao seu adjacente
        state_list = verify_adjacent_finger(states_=finger_states_copy, finger_name=finger,
                                            adjacent_finger=adjacent_finger, hand_fingers_points=hand_fingers_points)  # TODO: acompanhar estados

        # Atualiza dicionário com uma lista: o estado de cada dedo e se está próximo ou não do dedo adjacente
        finger_states.update({finger: state_list})

    return finger_states


def slope(x1, y1, x2, y2):
    """
    Calcula o coeficiente angular de dois pontos, ou seja, a variação no eixo y dividido
    pela variação no eixo x.
    :param x1: coordenada do primeiro ponto no eixo x
    :param y1: coordenada do primeiro ponto no eixo y
    :param x2: coordenada do segundo ponto no eixo x
    :param y2: coordenada do segundo ponto no eixo y
    :return: coeficiente angular
    """
    return (y2 - y1) / (x2 - x1)


def get_angle_between_two_lines(point1, point2, point3):
    """
    Calcula o ângulo entre duas retas através de três pontos passados como parâmetro.
    :param point1: tupla com as coordenadas x e y do primeiro ponto
    :param point2: tupla com as coordenadas x e y do segundo ponto
    :param point3: tupla com as coordenadas x e y do terceiro ponto
    :return: ângulo entre as duas retas em degrau
    """
    # Pontos
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    # Coeficiente angular da primeira reta
    m1 = slope(x1=x1, y1=y1, x2=x2, y2=y2)
    # print(m1)

    # Coeficiente angular da segunda reta
    m2 = slope(x1=x1, y1=y1, x2=x3, y2=y3)
    # print(m2)

    # Cálculo do ângulo
    angle_radians = math.atan((m2 - m1) / (1 + m1 * m2))

    # Conversão de radiano para degrau
    angle_degrees = round(math.degrees(angle_radians), 2)

    return angle_degrees


def get_angle(point1, point2, point3):
    """
    Calcula o ângulo interno de um triângulo passando três pontos, ou o ângulo entre uma
    reta formada pelos pontos 1 e 2 e reta formada pelos pontos 1 e 3.
    :param point1: tupla com as coordenadas x e y do primeiro ponto
    :param point2: tupla com as coordenadas x e y do segundo ponto
    :param point3: tupla com as coordenadas x e y do terceiro ponto
    :return: ângulo em degrau
    """
    # Pontos
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    # Variações no eixo y e x
    diff_y = y3 - y2
    diff_x = x3 - x1

    # Cálculo do ângulo
    angle_radians = math.atan(diff_y / diff_x)

    # Conversão de radiano para degrau
    angle_degrees = round(math.degrees(angle_radians), 2)

    return angle_degrees


def verify_hand_position(hand_direction, hand_fingers_points):
    """
    Verifica em que posição a mão se encontra com base em valor pré-determinado. Posição pode ser neutra (neutral)
    ou rotacionada (rotated).
    :param hand_direction: mão detectada
    :param hand_fingers_points: dicionário com as coordenadas (x, y, z) dos pontos de cada dedo da mão
    :return: posição da mão, neutra (neutral) ou rotacionada (rotated)
    """

    # Mão para cima
    if hand_direction == "up":

        # Primeiro ponto (base do dedo indicador)
        x1 = hand_fingers_points['index-finger']['x'][0]
        y1 = hand_fingers_points['index-finger']['y'][0]
        point1 = tuple((x1, y1))

        # Segundo ponto (base do dedo mínimo)
        x2 = hand_fingers_points['pinky']['x'][0]
        y2 = hand_fingers_points['pinky']['y'][0]
        point2 = tuple((x2, y2))

        # Terceiro ponto (ponto na horizontal)
        x3 = x2
        y3 = y1
        point3 = tuple((x3, y3))

        # print(f"Point1: ({point1}), point2: ({point2}) e point3: ({point3})")
        # hand_angle = get_angle_between_two_lines(point1=point1, point2=point2, point3=point3)
        # print(hand_angle)

        # Cálculo do ângulo
        angle = get_angle(point1=point1, point2=point2, point3=point3)
        # print(f"{abs(angle)}")

        if abs(angle) < THRESHOLD_ANGLE:  # Parâmetro ajustado através de testes
            return "neutral"
        else:
            return "rotated"

    # Mão para baixo
    else:  # TODO: possivelmente pode tirar esse if-else

        # Primeiro ponto (base do dedo indicador)
        x1 = hand_fingers_points['index-finger']['x'][0]
        y1 = hand_fingers_points['index-finger']['y'][0]
        point1 = tuple((x1, y1))

        # Segundo ponto (base do dedo mínimo)
        x2 = hand_fingers_points['pinky']['x'][0]
        y2 = hand_fingers_points['pinky']['y'][0]
        point2 = tuple((x2, y2))

        # Terceiro ponto (ponto na horizontal)
        x3 = x2
        y3 = y1
        point3 = tuple((x3, y3))

        # Cálculo do ângulo
        angle = get_angle(point1=point1, point2=point2, point3=point3)
        # print(f"{abs(angle)}")

        if abs(angle) < THRESHOLD_ANGLE:
            return "neutral"
        else:
            return "rotated"
