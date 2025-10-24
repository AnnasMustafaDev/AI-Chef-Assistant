from fastapi import FastAPI
from app.database.database import engine
from app.models import models
from app.routers import recipe_router

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Home Chef AI Assistant")

# Include routers
app.include_router(recipe_router.router, prefix="/api/v1", tags=["recipes"])

@app.get("/")
async def root():
    return {"message": "Welcome to Home Chef AI Assistant"}
