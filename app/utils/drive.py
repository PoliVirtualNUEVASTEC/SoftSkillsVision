import gdown
import os
import uuid

def download_video_from_drive(file_id: str, download_dir: str = "temp_videos") -> str:
    os.makedirs(download_dir, exist_ok=True)
    output_path = os.path.join(download_dir, f"{uuid.uuid4()}.mp4")
    url = f"https://drive.google.com/uc?id={file_id}"

    try:
        gdown.download(url, output_path, quiet=False)
        return output_path
    except Exception as e:
        raise RuntimeError(f"No se pudo descargar el video: {str(e)}")
