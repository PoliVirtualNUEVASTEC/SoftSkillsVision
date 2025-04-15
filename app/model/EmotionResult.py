from pydantic import BaseModel

class EmotionResult(BaseModel):
    emotion: str
    score: float
    