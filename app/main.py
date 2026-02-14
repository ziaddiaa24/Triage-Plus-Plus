from app.data.postgres import Base, engine
from app.data import models

Base.metadata.create_all(bind=engine)

from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Triage++",
    description="Intelligent Alert Triage Platform for SIEM",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "Triage++ running"}
