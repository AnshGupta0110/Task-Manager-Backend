from fastapi import FastAPI
from app.db import Base, engine
from app.routes import auth, tasks

# Create tables in MySQL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

# Include routers
app.include_router(auth.router)   # /register, /login etc.
app.include_router(tasks.router)  # /tasks endpoints

# Root endpoint
@app.get("/")
def root():
    return {"message": "Task Manager API with MySQL is running"}

# Test route to verify backend connection

@app.get("/test")
def test_connection():
    return {"message": "Backend connected!"}