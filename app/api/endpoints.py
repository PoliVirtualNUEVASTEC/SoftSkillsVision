from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.core.face_video_recog import process_video
from typing import List
from app.model.EmotionResult import EmotionResult

router = APIRouter()

@router.get("/procesar-video", response_model=List[EmotionResult])
def process_video_endpoint(
    video_path: str = Query(..., description="Ruta del video a procesar."),
    model_path: str = Query(..., description="Modelo a utilizar.")
) -> List[EmotionResult]:
    """
    Procesa un video para detectar emociones faciales y devuelve los resultados.
    
    - **video_path**: Ruta del video a procesar.
    - **model_path**: Ruta del modelo a utilizar.
    
    Devuelve una lista de resultados de emociones detectadas en el video.
    """
    return process_video(video_path, model_path)

@router.get("/analyze-video/")
def analyze_emotions():
    video_path = "D:/UNIVERSIDAD_1/SEMESTRE 2025 - 1/TRABAJO DE GRADO/SoftSkillsVision/SoftSkillsVision/PSICOLOGA_1_2025-03-27.mp4"
    model_path = "D:/UNIVERSIDAD_1/SEMESTRE 2025 - 1/TRABAJO DE GRADO/SoftSkillsVision/face_landmarker_v2_with_blendshapes.task"
    try:
        emotions = process_video(video_path, model_path)
        return JSONResponse(content={"emotions": emotions})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})