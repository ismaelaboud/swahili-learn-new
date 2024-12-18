from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, courses, enrollments, progress, lessons, assessments

app = FastAPI(title="Swahili Learn LMS", version="0.1.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(courses.router, prefix="/courses", tags=["courses"])
app.include_router(enrollments.router, prefix="/enrollments", tags=["enrollments"])
app.include_router(progress.router, prefix="/progress", tags=["progress"])
app.include_router(lessons.router)
app.include_router(assessments.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Swahili Learn LMS"}
