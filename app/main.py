from fastapi import FastAPI
from app.routers import auth, sessions
from app.database import engine, Base

app = FastAPI()

app.include_router(auth.router)
app.include_router(sessions.router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Interview prep bot is running"}
