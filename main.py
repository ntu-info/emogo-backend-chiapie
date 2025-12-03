from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from database import connect_to_mongo, close_mongo_connection
from routes import vlogs, sentiments, gps, export
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title="EmoGo Backend API",
    description="Backend API for EmoGo application - collecting vlogs, sentiments, and GPS data",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vlogs.router)
app.include_router(sentiments.router)
app.include_router(gps.router)
app.include_router(export.router)

# Mount videos directory for static file serving
videos_dir = os.path.join(os.path.dirname(__file__), "videos")
if os.path.exists(videos_dir):
    app.mount("/videos", StaticFiles(directory=videos_dir), name="videos")


@app.get("/")
async def root():
    return {
        "message": "Welcome to EmoGo Backend API",
        "version": "1.0.0",
        "documentation": "/docs",
        "export_page": "/export",
        "sample_video": "/videos/christmas.mp4"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}