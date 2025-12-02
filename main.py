from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import connect_to_mongo, close_mongo_connection
from routes import vlogs, sentiments, gps, export


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


@app.get("/")
async def root():
    return {
        "message": "Welcome to EmoGo Backend API",
        "version": "1.0.0",
        "documentation": "/docs",
        "export_page": "/export"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}