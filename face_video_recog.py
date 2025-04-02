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

# Función para dibujar los landmarks faciales en un frame
def draw_landmarks_on_image(rgb_image, detection_result):
    face_landmarks_list = detection_result.face_landmarks
    annotated_image = np.copy(rgb_image)
    for face_landmarks in face_landmarks_list:
        face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        face_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=lm.x, y=lm.y, z=lm.z) for lm in face_landmarks
        ])

        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style()
        )
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_contours_style()
        )
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_iris_connections_style()
        )
    return annotated_image

# Función para procesar video
def process_video(video_path, model_path):
    if not os.path.exists(video_path):
        print(f"Error: No se encontró el video '{video_path}'")
        return
    if not os.path.exists(model_path):
        print(f"Error: No se encontró el modelo '{model_path}'")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error al abrir el video")
        return

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
    emotion_detector = FER()

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
        if emotion:
            cv2.putText(annotated_frame, f"{emotion} ({score:.2f})", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            #print(f"EMOTION: {emotion}  SCORE: {score:.2f}")

        # Mostrar el frame anotado
        cv2.imshow("Video - Face Landmarks & Emotion", cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR))

        # Presiona 'q' para salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def get_files_from_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'C:/Users/carta/IdeaProjects/SoftSkillsVision/SoftSkillsVision/credentials.json'
    creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,scopes = SCOPES
    )
    service = build('drive', 'v3', credentials = creds) #Crear servicio de Google Drive
    folder_id = "1SIiUPEmfQCwFfO3JIqGRlWjIKkQBqQkw" #ID de la carpeta en Google Drive

    #Listando los archivos en la carpeta
    query =  f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    return files

def main():
    files_list = get_files_from_drive()
    video_path = "C:/Users/carta/IdeaProjects/SoftSkillsVision/SoftSkillsVision/THOR Y LOKI.mp4"
    model_path = "face_landmarker_v2_with_blendshapes.task"  #Ruta del modelo de MediaPipe
    process_video(video_path, model_path)

if __name__ == "__main__":
    main()
