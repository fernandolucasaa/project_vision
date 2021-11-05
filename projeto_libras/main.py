import os
import time
import cv2
import uuid
import numpy as np
import mediapipe as mp
from datetime import datetime as dt
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

# Câmera (imagem)
IMG_WIDTH, IMG_HEIGHT = 640, 480

# Dedos
HAND_FINGERS = ["thumb", "index-finger", "middle-finger", "ring-finger", "pinky"]

# Parâmetros do MediaPipe Hands
MAX_NUM_HANDS = 2  # Número máximo de mãos na imagem
MIN_DETECTION_CONFIDENCE = 0.8  # Nivel de confiança mínimo para detecção
MIN_TRACKING_CONFIDENCE = 0.5  # Nível de confiança mínimo para rastreio

# Parâmetros do desenho (retas e pontos)
LINE_COLOR = (121, 22, 76)
LINE_THICKNESS = 2
LINE_CIRCLE_RADIUS = 4
POINT_COLOR = (250, 44, 250)
POINT_THICKNESS = 2
POINT_CIRCLE_RADIUS = 2
# -------------------------


def display_webcam(filename=None):
    """
    Inicializa webcam. Para parar o processo pressionar o botão 'q' e para salvar o frame (imagem) na pasta OUTPUT_IMAGES_PATH
    pressione "s".
    """

    # Create a video capture object for the camera
    cap = cv2.VideoCapture(0)  # Maioria dos casos a câmera da webcam é 0
    print("Pressiona letra Q para terminar processo e S para salvar frame na pasta de saída.")

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
            # time.sleep(3)
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
                file_name = '{}.jpg'.format(uuid.uuid1())  # Nome únicoq
                cv2.imwrite(OUTPUT_IMAGES_PATH + file_name, cv2.flip(frame, 1))  # Salvar frame
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
    output = None

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

    # # Tratativa para apenas uma mão
    # if len(results.multi_hand_landmarks) == 1:
    #     # Mão detectada
    #     detected_hand = results.multi_handedness[0]
    #
    #     # Extrair informações (label e score)
    #     label = detected_hand.classification[0].label
    #     score = detected_hand.classification[0].score
    #     text = 'Label: {}, Score: {}'.format(label, round(score, 2))
    #
    #     # Extrair coordenadas de um ponto específico
    #     x = hand_landmarks.landmark[mark_name].x
    #     y = hand_landmarks.landmark[mark_name].y
    #
    #     # Cálculo de coordenadas
    #     multiply = np.multiply(np.array((x, y)), [IMG_WIDTH, IMG_HEIGHT])
    #     coords = tuple(multiply.astype(int))
    #
    #     output = text, coords
    #
    # else:
    #     # Mão detectada
    #     detected_hand = results.multi_handedness[index]
    #     # Extrair informações (label e score)
    #     label = detected_hand.classification[0].label
    #     score = detected_hand.classification[0].score
    #     text = 'Label: {}, Score: {}'.format(label, round(score, 2))
    #
    #     # Extrair coordenadas de um ponto específico
    #     x = hand_landmarks.landmark[mark_name].x
    #     y = hand_landmarks.landmark[mark_name].y
    #
    #     # Cálculo de coordenadas
    #     multiply = np.multiply(np.array((x, y)), [IMG_WIDTH, IMG_HEIGHT])
    #     coords = tuple(multiply.astype(int))
    #
    #     output = text, coords

        # Loop sobre cada mão detectada
        # for detected_hand in results.multi_handedness:
        #
        #     # Encontra a mão correta pelo índice
        #     if detected_hand.classification[0].index == index:  # TODO: corrigir aqui (verificar o que funciona)!!!
        #
        #         # Extrair informações (label e score)
        #         label = detected_hand.classification[0].label
        #         score = detected_hand.classification[0].score
        #         text = 'Label: {}, Score: {}'.format(label, round(score, 2))
        #
        #         # Extrair coordenadas de um ponto específico
        #         x = hand_landmarks.landmark[mark_name].x
        #         y = hand_landmarks.landmark[mark_name].y
        #
        #         # Cálculo de coordenadas
        #         multiply = np.multiply(np.array((x, y)), [IMG_WIDTH, IMG_HEIGHT])
        #         coords = tuple(multiply.astype(int))
        #
        #         output = text, coords

    return output


def process_image():
    # TODO: colocar uma descrição da função
    # Etapa 2.1: Ler imagem padrão
    print("Processar uma imagem padrão...")
    # img = cv2.imread(SAMPLE_IMAGE, 0)  # Grayscale
    # img = cv2.imread(SAMPLE_IMAGE, cv2.IMREAD_COLOR)

    # Ler imagem
    img = cv2.imread(SAMPLE_IMAGE)  # Imagem lida com formato BGR
    print(f"Shape da imagem lida: {img.shape}")

    cv2.imshow('Imagem padrao antes de processar', img)
    print("Pressione algum botão para continuar processo...")
    cv2.waitKey(0)  # Aguardar clicar algum botão do teclado
    cv2.destroyAllWindows()

    # Etapa 2.2: Instanciar solução (hands)
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

        # Dimensões da imagem
        IMG_HEIGHT, IMG_WIDTH, _ = img.shape

        # Faz uma cópia
        annotated_image = img.copy()

        if results.multi_hand_landmarks:  # Caso haja algum resultado

            # Mostrando resultados
            for num, hand_landmarks in enumerate(results.multi_hand_landmarks):  # Iteração em cada mão identificada

                # Desenhar as conexões na imagem cópia
                mp_drawing.draw_landmarks(annotated_image,
                                          hand_landmarks,
                                          mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                                          )

                # Mostra o label da mão
                if get_hand_informations(num, hand_landmarks, mp_hands.HandLandmark.WRIST, results):  # TODO: testar caso para duas mãos
                    text, coord = get_hand_informations(num, hand_landmarks, mp_hands.HandLandmark.WRIST, results)
                    print(f"Informações mão:\n"
                          f"- Geral: {text}\n"
                          f"- Pontos do ponto escolhido: {coord}")

                    # Mostrar na imagem o label e o score
                    cv2.putText(annotated_image,  # imagem
                                text,  # texto
                                coord,  # coordenada onde vai ser colocado o texto
                                cv2.FONT_HERSHEY_SIMPLEX,  # fonte
                                0.5,  # escala
                                (255, 255, 255),  # cor
                                1,  # Espessura
                                cv2.LINE_AA)

        #             # Mostrar na imagem as coordenadas de um ponto
        #             x_ = coord[0]
        #             y_ = coord[1] + 30
        #             coord_ = tuple((x_, y_))
        #             cv2.putText(annotated_image,  # imagem
        #                         str(coord),  # texto
        #                         coord_,  # coordenada onde vai ser colocado o texto
        #                         cv2.FONT_HERSHEY_SIMPLEX,  # fonte
        #                         0.4,  # escala
        #                         (255, 255, 255),  # cor
        #                         1,  # Espessura
        #                         cv2.LINE_AA)

            # Mostrar imagem com os tracejos (pontos e linhas)
            # annotated_image = cv2.flip(annotated_image, 1)  # TODO: entender caso, pq está invertido
            annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)  # BRG para RGB

            cv2.imshow('Imagem padrao processada (espelhado)', annotated_image)
            print("Pressione algum botão para continuar processo.")
            cv2.waitKey(0)  # Aguardar clicar algum botão do teclado
            cv2.destroyAllWindows()

        else:
            print("Não foi possível processar a imagem!")


def process_webcam_image():
    # TODO: colocar descrição da função

    # TODO: colocar prints explicando o que será feito

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

            # Converte BGR para RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Inverte na horizontal
            image = cv2.flip(image, 1)  # TODO: verificar se essa etapa é de fato necessária!!!

            # Para aumentar performance flag a imagem, será passada então como referência
            image.flags.writeable = False

            # Detecção
            results = hands.process(image)  # Imagem processada em RGB. Imagem processada é espelhada

            # Flag como true
            image.flags.writeable = True

            # Converte RGB para BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Volta para formato BGR

            # Mostrando resultados
            if results.multi_hand_landmarks:  # Caso haja algum resultado

                # Print handedness e desenha os contorno e linhas da mão
                print('Handedness:', results.multi_handedness)

                # Iteração em cada mão
                for num, hand in enumerate(results.multi_hand_landmarks):

                    # Desenhar as conexões em cada imagem (frame) da câmera
                    mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                              mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                                              )

                    # # Mostra o label da mão
                    if get_hand_informations(num, hand, mp_hands.HandLandmark.WRIST, results):
                        text, coord = get_hand_informations(num, hand, mp_hands.HandLandmark.WRIST, results)

                        # Mostrar na imagem o label e o score
                        cv2.putText(image,  # imagem
                                    text,  # texto
                                    coord,  # coordenada onde vai ser colocado o texto
                                    cv2.FONT_HERSHEY_SIMPLEX,  # fonte
                                    0.5,  # escala
                                    (255, 255, 255),  # cor
                                    1,  # Espessura
                                    cv2.LINE_AA)
                    #
                    #     # Mostrar na imagem as coordenadas de um ponto
                    #     x_ = coord[0]
                    #     y_ = coord[1] + 30
                    #     coord_ = tuple((x_, y_))
                    #     cv2.putText(image,  # imagem
                    #                 str(coord),  # texto
                    #                 coord_,  # coordenada onde vai ser colocado o texto
                    #                 cv2.FONT_HERSHEY_SIMPLEX,  # fonte
                    #                 0.4,  # escala
                    #                 (255, 255, 255),  # cor
                    #                 1,  # Espessura
                    #                 cv2.LINE_AA)

            # Mostrar imagem
            cv2.imshow('Hand tracking', image)

            # Sair do loop
            if cv2.waitKey(5) & 0xFF == ord('q'):  # Pressionar 'q' para sair
                # Salvar imagem com nome único
                file_name = '{}.jpg'.format(uuid.uuid1())  # Nome único
                # cv2.imwrite(OUTPUT_IMAGES_PATH + file_name, image)  # Salvar frame
                break

    # Libera recursos alocados
    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':

    # MediaPipe Hand
    # mp_drawing_styles = mp.solutions.drawing_styles  # TODO: entender pq nao funciona. Talvez mudou o nome do metodo ?
    print("Inicializando processo...")
    mp_hands = mp.solutions.hands  # Solução para detecção e rastreio de mão e dedos
    mp_drawing = mp.solutions.drawing_utils  # Solução para desenhos das conexões entre os pontos

    # Etapa 1: Escolher ação a ser processado (imagem ou vídeo)
    # print("Olá. Deseja processar uma imagem (1) ou o vídeo de sua câmera do notebook (2) ou acessar a webcam do seu notebook (3) ?")

    flag = False
    modes = ["1", "2", "3"]  # Opções aceitas
    start_time = dt.now()  # Início do processo
    max_time = 1*60  # Máximo de tempo esperando uma entrada

    option = "1"  # Imagem  # TODO: provisório
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

    # Etapa 2: Executar ação escolhida
    if option == "1":  # Processar imagem (ler pontos chaves da mão)
        process_image()

    elif option == "2":  # Processar vídeo da câmera webcam
        process_webcam_image()  # TODO: investigando esse caso para duas mãos

    elif option == "3":  # Acessar webcam do notebook
        display_webcam()

    print("Processo finalizado. Até a próxima :)")

    # # Etapa 1: Determinar imagem a ser processada
    # file = input_images_path + "letra_a_img.jpg"
    #
    # # Ler imagem, invertê-la na horizontal
    # img = cv2.imread("images/letra_a_img.jpg")
    #
    # img = cv2.flip(cv2.imread(file), 1)  # Imagem lida com formato BGR
    # cv2.imshow('Exemplo de deteccao e rastreio de maos e dedos', img)
    # cv2.waitKey(0)  # Clica botão teclado
    # cv2.destroyAllWindows()
    #
    # # Etapa 2: Instanciar solução (hands) e processar imagem
    # # hands = mp_hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.8, min_tracking_confidence=0.5)
    #
    # with mp_hands.Hands(
    #         static_image_mode=True,  # Modo para entrada imagem
    #         max_num_hands=2,  # Número máximo de mãos na imagem
    #         min_detection_confidence=0.8,  # Nivel de confiança mínimo para detecção
    #         min_tracking_confidence=0.5,  # Nível de confiança mínimo para rastreio
    # ) as hands:
    #
    #     # Ler imagem, invertê-la na horizontal
    #     img = cv2.flip(cv2.imread(file), 1)  # Imagem lida com formato BGR
    #
    #     # Converte imagem antes de processa-la
    #     results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # Imagem processa em formato RBG
    #
    #     # Print handedness e desenha os contorno e linhas da mão
    #     print('Handedness:', results.multi_handedness)
    #
    #     # Dimensões da imagem
    #     image_height, image_width, _ = img.shape
    #
    #     # Faz uma cópia
    #     annotated_image = img.copy()
    #
    #     # Mostrando resultados
    #     for num, hand_landmarks in enumerate(results.multi_hand_landmarks):  # Iteração em cada mão identificada
    #
    #         # print('hand_landmarks:', hand_landmarks)
    #         print(
    #             f'Index finger tip coordinates: (',
    #             f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
    #             f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
    #         )
    #
    #         # Desenhar as conexões na imagem cópia
    #         mp_drawing.draw_landmarks(annotated_image,
    #                                   hand_landmarks,
    #                                   mp_hands.HAND_CONNECTIONS
    #                                   # mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
    #                                   # mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
    #                                   )
    #
    #         # Mostra o label da mão
    #         if get_informations_hand(num, hand_landmarks, mp_hands.HandLandmark.WRIST, results):  # TODO: não está funcionando!
    #             text, coord = get_informations_hand(num, hand_landmarks, mp_hands.HandLandmark.WRIST, results)
    #             print(text, coord)
    #
    #             # Mostrar na imagem o label e o score
    #             cv2.putText(annotated_image,  # imagem
    #                         text,  # texto
    #                         coord,  # coordenada onde vai ser colocado o texto
    #                         cv2.FONT_HERSHEY_SIMPLEX,  # fonte
    #                         0.5,  # escala
    #                         (255, 255, 255),  # cor
    #                         1,  # Espessura
    #                         cv2.LINE_AA)
    #
    #             # Mostrar na imagem as coordenadas de um ponto
    #             x_ = coord[0]
    #             y_ = coord[1] + 30
    #             coord_ = tuple((x_, y_))
    #             cv2.putText(annotated_image,  # imagem
    #                         str(coord),  # texto
    #                         coord_,  # coordenada onde vai ser colocado o texto
    #                         cv2.FONT_HERSHEY_SIMPLEX,  # fonte
    #                         0.4,  # escala
    #                         (255, 255, 255),  # cor
    #                         1,  # Espessura
    #                         cv2.LINE_AA)
