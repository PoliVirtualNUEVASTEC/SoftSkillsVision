import os
import numpy as np
import cv2
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import matplotlib.pyplot as plt
from fer import FER

#draw_landmarks_on_image: se encarga de dibujar los puntos de referencia faciales en la imagen
def draw_landmarks_on_image(rgb_image, detection_result):
    face_landmarks_list = detection_result.face_landmarks
    annotated_image = np.copy(rgb_image)
    #DOCUMENTAR
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

#proccess_image: Carga una imagen, utilizando el modelo de MediaPipe para detectar los puntos de referencia faciales y luego
#muestra la imagen anotada con los puntos de referencia faciales dibujados
def process_image(image_path, model_path):
    if not os.path.exists(image_path):
        print(f"Error: No se encontró la imagen '{image_path}'")
        return
    if not os.path.exists(model_path):
        print(f"Error: No se encontró el modelo '{model_path}'")
        return

    img = cv2.imread(image_path)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        output_face_blendshapes=True,
        output_facial_transformation_matrixes=True,
        num_faces=1
    )
    detector = vision.FaceLandmarker.create_from_options(options)

    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)
    detection_result = detector.detect(image)
    annotated_image = draw_landmarks_on_image(rgb_img, detection_result)

    cv2.imshow("Face Landmarks Image", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    #-----------------Emotion Detection-----------------
    #Detectar emoción con FER
    emotion, score = detect_emotion(rgb_img)
    if emotion:
        cv2.putText(annotated_image, f"{emotion} ({score:.2f})", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("Face Landmarks & Emotion", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def detect_emotion(image):
    detector = FER()
    emotion, score = detector.top_emotion(image)
    return emotion, score

#La función main especifica la ruta de la imagen y del modelo, y llama a process_image para procesar la imagen.
def main():
    image_path = "image1.png"
    model_path = "face_landmarker_v2_with_blendshapes.task"
    process_image(image_path, model_path)

    """
    
    list_image_path = ["image1.png", "image2.png", "image3.png"]
    for image_path in list_image_path:
        process_image(image_path, model_path)
    """

if __name__ == "__main__":
    main()