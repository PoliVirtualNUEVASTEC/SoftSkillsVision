from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.core.face_video_recog import process_video
from app.core.face_video_recog import get_files_from_drive
from typing import List
from app.model.EmotionResult import EmotionResult
from fastapi import APIRouter, HTTPException
from app.utils.drive import download_video_from_drive
import os

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

@router.get("/analyze-drive")
def analyze_emotions_from_drive(file_id: str):
    list_videos_from_drive = get_files_from_drive(file_id)
    model_path = r"F:/Documents/GitHub/SoftSkillsVision/face_landmarker_v2_with_blendshapes.task"
    resultado = []
    for video in list_videos_from_drive:
        try:           
            video_path = download_video_from_drive(video["id"])            
            emotions = process_video(video_path, model_path)
            os.remove(video_path)
            resultado.append({
                "id": video["id"],
                "nombre": video["name"],
                "emociones": emotions
            })
            #JsonResponse =  JSONResponse(content={"emotions": emotions})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return resultado
    
