import os
import time
import cv2
import uuid
import numpy as np
import mediapipe as mp
from datetime import datetime as dt
import calculations
import alphabet

# import matplotlib.pyplot as plt

# --- Variáveis globais ---
# Gerais
path = os.path.dirname(os.path.abspath(__file__))  # TODO: padronizar
path = os.path.abspath(os.path.join(path, os.pardir))  # Diretório acima
INPUT_IMAGES_PATH = path + '\\images\\'
OUTPUT_IMAGES_PATH = path + '\\output_images\\'
SAMPLE_IMAGE = INPUT_IMAGES_PATH + "letra_a_img_mao_direita.jpg"
# SAMPLE_IMAGE = INPUT_IMAGES_PATH + "letra_a_img_mao_esquerda.jpg"
# SAMPLE_IMAGE = INPUT_IMAGES_PATH + "letra_a_img_duas_maos.jpg"

# Dimensões da imagem lida (padrão)
IMG_WIDTH, IMG_HEIGHT = 640, 480

# Dedos
HAND_FINGERS = ["thumb", "index-finger", "middle-finger", "ring-finger", "pinky"]

# Parâmetros do MediaPipe Hands
MAX_NUM_HANDS = 2  # Número máximo de mãos na imagem
MIN_DETECTION_CONFIDENCE = 0.8  # Nivel de confiança mínimo para detecção
MIN_TRACKING_CONFIDENCE = 0.5  # Nível de confiança mínimo para rastreio

# Parâmetros do desenho (retas e pontos)
LINE_COLOR = (121, 22, 76)  # BGR (Blue, Green, Red)
LINE_THICKNESS = 2
LINE_CIRCLE_RADIUS = 4

POINT_COLOR = (0, 0, 255)  # BGR
POINT_THICKNESS = 2
POINT_CIRCLE_RADIUS = 2

# Parâmetros de texto
TEXT_SCALE = 0.5
TEXT_COLOR = (255, 255, 255)  # BGR
TEXT_THICKNESS = 1


# -------------------------


def display_webcam(filename=None):
    """
    Inicializa webcam. Para parar o processo pressionar o botão 'q' e para salvar o frame (imagem) na pasta OUTPUT_IMAGES_PATH
    pressione "s".
    """

    # Create a video capture object for the camera
    cap = cv2.VideoCapture(0)  # Maioria dos casos a câmera da webcam é 0
    print("Pressione letra Q para terminar processo e letra S para salvar frame na pasta de saída.")

    try:
        while True:
            # Capture the video frame-by-frame
            _, frame = cap.read()

            # Flip the image
            frame = cv2.flip(frame, 1)

            # Display the resulting frame
            cv2.imshow('Frame', frame)

            # # Salvar imagem
            # print("Salvar frame...")
            # count = 0
            # while count <= 3:
            #     print(f"Salvando em : {(3-count)}s")
            #     time.sleep(1)
            #     count += 1
            # file_name = '{}.jpg'.format(uuid.uuid1())  # Nome únicoq
            # cv2.imwrite(OUTPUT_IMAGES_PATH + file_name, cv2.flip(frame, 1))  # Salvar frame
            # print("Frame salvo.")

            # Press 'q' button to quit and 's' button to save the image
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Terminando processo...")
                break
            elif cv2.waitKey(1) & 0xFF == ord('s'):
                # Salvar imagem com nome único
                print("Salvando frame...")
                file_name = '{}.jpg'.format(uuid.uuid1())  # Nome único
                cv2.imwrite(OUTPUT_IMAGES_PATH + file_name, cv2.flip(frame, 1))  # Salvar frame (inverte imagem para orientação correta)
                print("Frame salvo.")
                # break

        # Release the capture
        cap.release()
        cv2.destroyAllWindows()
    except:
        # Release the capture
        cap.release()
        cv2.destroyAllWindows()


def get_hand_informations(index, hand_landmarks, mark_name, results):
    """
    Retorna um texto com o label (left ou right) e o score para uma mão específica (índice), e
    as coordenadas x e y desta mão para um ponto da mão específico.
    """

    # Mão detectada
    detected_hand = results.multi_handedness[index]

    # Extrair informações (label e score)
    label = detected_hand.classification[0].label
    score = detected_hand.classification[0].score
    text = 'Label: {}, Score: {}'.format(label, round(score, 2))

    # Extrair coordenadas de um ponto específico
    x = hand_landmarks.landmark[mark_name].x
    y = hand_landmarks.landmark[mark_name].y

    # Cálculo de coordenadas
    multiply = np.multiply(np.array((x, y)), [IMG_WIDTH, IMG_HEIGHT])
    coords = tuple(multiply.astype(int))

    output = text, coords

    return output


def process_image():
    """
    Lê uma imagem padrão (input) e aplica a solução de rastreio e detecção de pontos da mão na imagem da webcam. Faz o cortorno dos pontos detectados
    e coloca na imagem algumas informações básicas.
    """
    print("Processar uma imagem padrão...")

    # Ler imagem padrão
    img = cv2.imread(SAMPLE_IMAGE)  # Imagem lida com formato BGR
    # img = cv2.imread(SAMPLE_IMAGE, 0)  # Grayscale

    # Dimensões da imagem
    IMG_HEIGHT, IMG_WIDTH, _ = img.shape
    print(f"Shape da imagem lida: {img.shape}")

    # Mostrar imagem
    cv2.imshow('Imagem padrao antes', img)

    print("Pressione algum botão para continuar o processo...")
    cv2.waitKey(0)  # Aguardar clicar algum botão do teclado
    cv2.destroyAllWindows()

    # Instanciar solução (hands)
    with mp_hands.Hands(
            static_image_mode=True,  # Modo para entrada imagem
            max_num_hands=MAX_NUM_HANDS,  # Número máximo de mãos na imagem
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,  # Nivel de confiança mínimo para detecção
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,  # Nível de confiança mínimo para rastreio
    ) as hands:

        # Inverte imagem na horizontal
        img = cv2.flip(img, 1)

        # Converte imagem
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BRG para RGB

        # Processa a imagem
        results = hands.process(img)  # Imagem processa em formato RBG

        # Print handedness e desenha os contorno e linhas da mão
        # print('Handedness:', results.multi_handedness)

        # Faz duas cópia
        annotated_image = img.copy()
        annotated_image_2 = img.copy()

        # TODO: é possível fazer melhorias nas funções abaixo (modularizar mais ainda)
        if results.multi_hand_landmarks:  # Caso haja algum resultado

            # Mostrando resultados
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):  # Iteração em cada mão identificada

                # Desenhar as conexões (linhas e pontos) na imagem cópia
                mp_drawing.draw_landmarks(annotated_image,
                                          hand_landmarks,
                                          mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                                          )

                # Desenhar as conexões (linhas e pontos) na imagem cópia
                mp_drawing.draw_landmarks(annotated_image_2,
                                          hand_landmarks,
                                          mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                                          )

                # Mostra o label da mão
                if get_hand_informations(i, hand_landmarks, mp_hands.HandLandmark.WRIST, results):  # TODO: melhoria: deixar esse ponto como um parâmetro global

                    # Extrai o label e o score da mão detectada, e as coordenadas do ponto passada como parâmetro
                    text, coord = get_hand_informations(i, hand_landmarks, mp_hands.HandLandmark.WRIST, results)

                    print(f"Informações da mão detectada:\n"
                          f"- Geral: {text}\n"
                          f"- Coordenadas do ponto escolhido: {coord}")

                    # Mostra na imagem (frame) as informações extraídas
                    display_informations(annotated_image, text, coord, str(mp_hands.HandLandmark.WRIST).split('.')[1])

            # Inverte imagem já com os tracejos
            annotated_image_2 = cv2.flip(annotated_image_2, 1)

            # Iteração em cada mão
            for i, hand in enumerate(results.multi_hand_landmarks):
                # Extrai o label e o score da mão detectada, e as coordenadas do ponto passada como parâmetro
                text, coord = get_hand_informations(i, hand, mp_hands.HandLandmark.WRIST, results)

                # Alterações para salvar imagem com informações na orientação espelhada (correta)
                x_, y_ = coord
                x_ = IMG_WIDTH - x_
                coord_ = tuple((x_, y_))

                # Mostra na imagem (frame) as informações extraídas
                display_informations(annotated_image_2, text, coord_, str(mp_hands.HandLandmark.WRIST).split('.')[1])

            # Converter padrão de cores
            annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)  # BRG para RGB
            annotated_image_2 = cv2.cvtColor(annotated_image_2, cv2.COLOR_BGR2RGB)  # BRG para RGB

            # Mostrar imagem com os tracejos (pontos e linhas)
            cv2.imshow('Imagem padrao processada (espelhado)', annotated_image)
            cv2.imshow('Imagem padrao processada (sentido correto)', annotated_image_2)

            # Finalizar processo
            print("Pressione algum botão para continuar e terminar o processo.")
            cv2.waitKey(0)  # Aguardar clicar algum botão do teclado
            cv2.destroyAllWindows()

        else:
            print("Não foi possível processar a imagem!")


def display_informations(image, text, coord, mark_name=None):
    """
    Mostrar informações (texto) em uma imagem em uma posição definida. As informações a serem mostradas
    são o label e o score da mão detectada, e as coordenadas de um ponto chave específico.
    """

    # Mostrar na imagem o label e o score
    cv2.putText(image,  # imagem
                text,  # texto
                coord,  # coordenada onde vai ser colocado o texto
                cv2.FONT_HERSHEY_SIMPLEX,  # fonte
                TEXT_SCALE,  # escala
                TEXT_COLOR,  # cor
                TEXT_THICKNESS,  # Espessura
                cv2.LINE_AA)

    # Mostrar na imagem as coordenadas de um ponto
    x_ = coord[0]
    y_ = coord[1] + 30

    coord_ = tuple((x_, y_))
    text_ = str(coord)
    if mark_name is not None:
        text_ = mark_name + ' ' + str(coord)

    cv2.putText(image,  # imagem
                text_,  # texto
                coord_,  # coordenada onde vai ser colocado o texto
                cv2.FONT_HERSHEY_SIMPLEX,  # fonte
                TEXT_SCALE - 0.1,  # escala
                TEXT_COLOR,  # cor
                TEXT_THICKNESS,  # Espessura
                cv2.LINE_AA)


def display_calculated_informations(image, information, coord=None):
    """
    Mostrar informações extraídas do modelo
    :param image:
    :param information:
    :return:
    """

    text = "Informations:"
    cv2.putText(image, text, tuple((20, 20)),
                cv2.FONT_HERSHEY_SIMPLEX, TEXT_SCALE - 0.2,
                TEXT_COLOR, TEXT_THICKNESS, cv2.LINE_AA)

    if coord is None:
        coord = tuple((20, 30))

    text = information
    cv2.putText(image,  # imagem
                text,  # texto
                coord,  # coordenada onde vai ser colocado o texto
                cv2.FONT_HERSHEY_SIMPLEX,  # fonte
                TEXT_SCALE - 0.2,  # escala
                TEXT_COLOR,  # cor
                TEXT_THICKNESS,  # Espessura
                cv2.LINE_AA)


def display_identified_letter(image, identified_letter, img_width):
    text = "Letra identificada: " + identified_letter
    x = int(img_width / 2) - 100
    coord = tuple((x, 35))  # Coordenadas (x,y)
    cv2.putText(image, text, coord,
                cv2.FONT_HERSHEY_SIMPLEX, TEXT_SCALE + 0.2,
                TEXT_COLOR, TEXT_THICKNESS, cv2.LINE_AA)


def process_webcam_image():
    """
    Aplica a solução de rastreio e detecção de pontos da mão na imagem da webcam. Faz o cortorno dos pontos detectados
    e coloca na imagem algumas informações básicas.
    """

    print("Iniciando processo de aplicar solução de detecção e rastreio de ponto da mão na imagem de webcam...")
    print("Pressione letra Q para terminar processo e letra S para salvar frame na pasta de saída.")

    cap = cv2.VideoCapture(0)  # Maioria dos casos a câmera do webcam é 0

    # Comando 'with' garante que os recursos sejam fechados após a execução do bloco
    with mp_hands.Hands(
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,  # Nivel de confiança mínimo para detecção
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,  # Nível de confiança mínimo para rastreio
    ) as hands:

        # Enquanto a câmera está aberta
        while cap.isOpened():
            # Leitura da imagem da câmera
            _, frame = cap.read()  # Frame é lido em formato BGR

            # Dimensões da imagem
            IMG_HEIGHT, IMG_WIDTH, _ = frame.shape

            # Converte BGR para RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Inverte na horizontal
            image = cv2.flip(image, 1)

            # Para aumentar performance marque (flag) a imagem, esta será passada então como referência
            image.flags.writeable = False

            # Detecção
            results = hands.process(image)  # Imagem processada em RGB. Imagem processada dever ser espelhada!
            # Obs.: Nos testes foi observado que se não fizer isso identifica a mão como contrária!

            # Flag como true
            image.flags.writeable = True

            # Converte RGB para BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Volta para formato BGR

            # Cópia para inverter imagem
            img_copy = image.copy()

            # Mostrando resultados
            if results.multi_hand_landmarks:  # Caso haja algum resultado

                # Print handedness e desenha os contorno e linhas da mão
                # print('Handedness:', results.multi_handedness)

                # Iteração em cada mão
                for i, hand in enumerate(results.multi_hand_landmarks):

                    # Desenhar as conexões (linhas e pontos) em cada imagem (frame) da câmera
                    mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=POINT_COLOR, thickness=POINT_THICKNESS, circle_radius=POINT_CIRCLE_RADIUS),
                                              mp_drawing.DrawingSpec(color=LINE_COLOR, thickness=LINE_THICKNESS, circle_radius=LINE_CIRCLE_RADIUS)
                                              )

                    # Faz uma cópia apenas com os trações feitos (para salvar imagem em orientação correta)
                    mp_drawing.draw_landmarks(img_copy, hand, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=POINT_COLOR, thickness=POINT_THICKNESS, circle_radius=POINT_CIRCLE_RADIUS),
                                              mp_drawing.DrawingSpec(color=LINE_COLOR, thickness=LINE_THICKNESS, circle_radius=LINE_CIRCLE_RADIUS)
                                              )

                    # Mostrar informações da mão detectada
                    if get_hand_informations(i, hand, mp_hands.HandLandmark.WRIST, results):
                        # Extrai o label e o score da mão detectada, e as coordenadas do ponto passada como parâmetro
                        text, coord = get_hand_informations(i, hand, mp_hands.HandLandmark.WRIST, results)

                        # Mostra na imagem (frame) as informações extraídas
                        display_informations(image, text, coord, str(mp_hands.HandLandmark.WRIST).split('.')[1])

                    # --- Extrair informações da mão e dedos ---  # TODO: associar informações a cada mão !!!
                    # 1. Direção da mão
                    hand_direction = calculations.verify_hand_direction(hand=hand)
                    # print(hand_direction)

                    # 2. Pontos ds dedos
                    hand_fingers_points = calculations.extract_finger_points(hand=hand, img_height=IMG_HEIGHT, img_width=IMG_WIDTH)
                    # print(hand_fingers_points)

                    # 3. Estados dos dedos
                    hand_fingers_states = calculations.verify_hand_fingers_states(hand=hand, img_height=IMG_HEIGHT, hand_direction=hand_direction,
                                                                                  hand_fingers_points=hand_fingers_points)  # TODO: melhorar
                    print(hand_fingers_states)

                    # 4. Face da mão voltada (palma ou costas da mão)
                    hand_side = calculations.verify_hand_side_foward(label=results.multi_handedness[i].classification[0].label.lower(),
                                                                     hand=hand, hand_direction=hand_direction)
                    # print(hand_side)

                    # 5. Verificar se mão está em posição neutra
                    hand_position = calculations.verify_hand_position(hand_direction=hand_direction, hand_fingers_points=hand_fingers_points)
                    # print(hand_angle)

                    # --- Testes para ajustar parâmetros ---
                    # diference_thumb = calculations.compute_thumb_diference(hand_fingers_points=hand_fingers_points)
                    # diference_thumb = round(diference_thumb, 2)
                    # finger_distance = calculations.compute_distance_adjacent_finger(finger_name=HAND_FINGERS[1], adjacent_finger=HAND_FINGERS[2], hand_fingers_points=hand_fingers_points)
                    # finger_distance = round(finger_distance, 2)
                    # thumb_distance = calculations.compute_distance_adjancent_finger_thumb(hand_fingers_points=hand_fingers_points)
                    # thumb_distance = round(thumb_distance, 2)
                    # length = calculations.compute_reference_value(hand_fingers_points=hand_fingers_points)
                    # length = round(length, 2)
                    # display_calculated_informations(image=image, information=f"Thumb distance: {thumb_distance}", coord=tuple((20, 60)))
                    # --------------------------------------

                    # Mostrar características determinada
                    display_calculated_informations(image=image, information=f"Hand direction: {hand_direction}")
                    display_calculated_informations(image=image, information=f"Hand side: {hand_side}", coord=tuple((20, 40)))
                    display_calculated_informations(image=image, information=f"Hand position: {hand_position}", coord=tuple((20, 50)))

                    # --- Indentificar letra ---
                    hand_state = {
                        'direction': hand_direction,
                        'side': hand_side,
                        'position': hand_position,
                        'label': results.multi_handedness[i].classification[0].label.lower(),
                        'fingers_states': hand_fingers_states
                    }
                    letter = alphabet.identify_letter(alphabet_letters=alphabet.AlphabetLetters, states=hand_state)  # TODO: preencher características de mais letras do alfabeto !
                    # print(letter)
                    display_identified_letter(image=image, identified_letter=letter, img_width=IMG_WIDTH)
                    # --------------------------

                # Inverte imagem já com os tracejos
                image_copy = cv2.flip(img_copy, 1)

                # Iteração em cada mão
                for i, hand in enumerate(results.multi_hand_landmarks):
                    # Extrai o label e o score da mão detectada, e as coordenadas do ponto passada como parâmetro
                    text, coord = get_hand_informations(i, hand, mp_hands.HandLandmark.WRIST, results)

                    # Alterações para salvar imagem com informações na orientação espelhada (correta)
                    x_, y_ = coord
                    x_ = IMG_WIDTH - x_
                    coord_ = tuple((x_, y_))

                    # Mostra na imagem (frame) as informações extraídas
                    display_informations(image_copy, text, coord_, str(mp_hands.HandLandmark.WRIST).split('.')[1])

                # cv2.imshow("Hand tracking (mirrored)", image_copy)

            # Mostrar imagem
            cv2.imshow('Hand tracking', image)

            # Sair do loop
            if cv2.waitKey(1) & 0xFF == ord('s'):  # Pressione 's' para salvar frame
                # Salvar imagem com nome único
                file_name = '{}.jpg'.format(uuid.uuid1())  # Nome único
                cv2.imwrite(OUTPUT_IMAGES_PATH + file_name, image_copy)  # Salvar frame
            elif cv2.waitKey(1) & 0xFF == ord('q'):  # Pressione 'q' para sair
                print("Terminando processo...")
                break

    # Liberar recursos alocados
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    # MediaPipe Hand
    # mp_drawing_styles = mp.solutions.drawing_styles  # TODO: entender pq nao funciona. Talvez mudou o nome do método ?
    print("Inicializando processo...")
    mp_hands = mp.solutions.hands  # Solução para detecção e rastreio de mão e dedos
    mp_drawing = mp.solutions.drawing_utils  # Solução para desenhos das conexões entre os pontos

    # Etapa 1: Escolher ação a ser processado (imagem ou vídeo)
    # print("Olá. Deseja processar uma imagem (1) ou o vídeo de sua câmera do notebook (2) ? Ou apenas acessar a webcam "
    #       "do seu notebook (3) sem aplica a solução do MediaPipe Hands ?")

    flag = False
    modes = ["1", "2", "3"]  # Opções aceitas
    start_time = dt.now()  # Início do processo
    max_time = 1 * 60  # Máximo de tempo esperando uma entrada

    option = "2"  # TODO: provisório
    # while flag is False and (dt.now() - start_time).seconds < max_time:  # TODO: decomentar
    #     option = input("Escolher opção: ...")
    #     print("Analisando escolha")
    #     if option is not None:  # Alguma entrada lida
    #         if option not in modes:
    #             print("Por favor, inserir uma entrada válida")
    #         else:
    #             print("Escolha aceita!")
    #             flag = True
    # else:
    #     print("Processo finalizado, não foi feito uma escolha correta. Até a próxima :)")
    #     exit()

    # Etapa 2: Executar ação escolhidaqq
    if option == "1":  # Processar imagem (ler pontos chaves da mã, aplicar solução MediaPipe Hands)
        process_image()  # Imagem processada é mostrada

    elif option == "2":  # Processar vídeo da câmera webcam (aplicar solução MediaPipe Hands)
        process_webcam_image()  # Possível salvar o frame

    elif option == "3":  # Apenas acessar webcam do notebook
        display_webcam()  # Possível salvar o frame

    print("Processo finalizado. Até a próxima :)")
