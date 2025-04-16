import os
import numpy as np
import cv2
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from fer import FER
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
import math
# Función para dibujar los landmarks faciales en un frame

""" 
Este script utiliza la librería MediaPipe para detectar landmarks faciales y la librería FER para detectar emociones en un video.
"""
emotions_dict = {
    "neutral" : "NEUTRO",
    "happy" : "FELIZ",
    "sad" : "TRISTE",
    "angry" : "ENFADADO",
    "fear": "MIEDO",
    "disgust" : "ASCO",
    "surprise": "SORPRESA",
}
def draw_landmarks_on_image(rgb_image, detection_result):
    """Utiliza MediaPipe para detectar landmarks faciales y dibujarlos en cada frame del video."""
    face_landmarks_list = detection_result.face_landmarks
    annotated_image = np.copy(rgb_image)
    for face_landmarks in face_landmarks_list:
        face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        face_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=lm.x, y=lm.y, z=lm.z) for lm in face_landmarks
        ])
        # Dibuja la malla facial
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style()
        )
        # Dibuja los contornos faciales
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_contours_style()
        )
        # Dibuja los iris
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_iris_connections_style()
        )
    return annotated_image

"""Cada frame del video se procesa para:
    1. Convertirlo de formato BGR a RGB.
    2. Detectar los landmarks faciales utilizando MediaPipe.
    3. Detectar la emoción utilizando la librería FER.
    4. Dibujar los landmarks y la emoción detectada en el frame, en una ventana emergente"""
def process_video(video_path, model_path):
    emotions_detected = []
    score_detected = []
    emotion_detector = FER()

    if not os.path.exists(video_path) or not os.path.exists(model_path):
        return []
     
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        #print("Error al abrir el video")
        return[]

    # Inicializar el detector de landmarks faciales de MediaPipe
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        output_face_blendshapes=True,
        output_facial_transformation_matrixes=True,
        num_faces=1
    )
    detector = vision.FaceLandmarker.create_from_options(options)

    # Inicializar el detector de emociones de FER
    
    """ Se utiliza la librería FER para detectar emociones en el video."""
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir de BGR a RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # Detección de landmarks faciales
        detection_result = detector.detect(image)
        annotated_frame = draw_landmarks_on_image(rgb_frame, detection_result)

        # Detección de emoción con FER
        emotion, score = emotion_detector.top_emotion(rgb_frame)
        if (emotion == None) and (score == None):
            print("No se detectó emoción")
        else:
            emotions_detected.append(emotion)
            score_detected.append(score)
        
        if emotion:
            cv2.putText(annotated_frame, f"{emotions_dict.get(emotion)}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (244, 211, 49), 2, cv2.LINE_AA)
            #print(f"EMOTION: {emotion}  SCORE: {score:.2f}")

        # Mostrar el frame anotado
        #cv2.imshow("Video - Face Landmarks & Emotion", cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR))

        # Presiona 'q' para salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

   
    cap.release()
    cv2.destroyAllWindows()
    json_to_return = [{"emotion": emo, "score": sc} for emo, sc in zip(emotions_detected, score_detected)]
    return json_to_return

def get_files_from_drive(folder_id:str):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'D:/UNIVERSIDAD_1/SEMESTRE 2025 - 1/TRABAJO DE GRADO/SoftSkillsVision/SoftSkillsVision/credentials.json'
    creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,scopes = SCOPES
    )
    service = build('drive', 'v3', credentials = creds) #Crear servicio de Google Drive
    #folder_id = "1SIiUPEmfQCwFfO3JIqGRlWjIKkQBqQkw" #ID de la carpeta en Google Drive

    #Listando los archivos en la carpeta
    query =  f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    return files

def main():
    files_list = get_files_from_drive()
    video_path = "D:/UNIVERSIDAD_1/SEMESTRE 2025 - 1/TRABAJO DE GRADO/SoftSkillsVision/SoftSkillsVision/PSICOLOGA_1_2025-03-27.mp4"
    model_path = "face_landmarker_v2_with_blendshapes.task"  #Ruta del modelo de MediaPipe
    process_video(video_path, model_path)


"""
Flujo general del script:
1. Carga del video: Se verifica que el archivo de video y el modelo existan.
2. Inicialización de detectores:
   - Detector de landmarks faciales de MediaPipe.
   - Detector de emociones de FER.
3. Procesamiento frame por frame:
   - Detección de landmarks faciales y dibujo de estos en el frame.
   - Detección de emociones y superposición del texto correspondiente.
   - Visualización del video procesado.
4. Conexión a Google Drive: Lista los archivos en una carpeta específica (aunque no interactúa con ellos en el flujo principal).
"""
"""CV2 Se utiliza para:
        1. Lectura del video. cap = cv2.VideoCapture(video_path)
        2. Conversión de BGR a RGB. rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        3. Superposición de texto en el frame.  cv2.putText(annotated_frame, f"{emotion} ({score:.2f})", (50, 50),
                                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        4. Visualización del video procesado. cv2.imshow("Video - Face Landmarks & Emotion", cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR))
        5. Control del flujo del video.     if cv2.waitKey(1) & 0xFF == ord('q'):
                                                break
        6. Liberación de recursos al finalizar el procesamiento.
            cap.release()
            cv2.destroyAllWindows()
        """