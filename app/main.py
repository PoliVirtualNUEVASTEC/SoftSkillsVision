from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(title="Soft Skills Vision API", 
              description="API for Soft Skills Vision",
              version="1.0.0")

app.include_router(endpoints.router)