from fastapi import FastAPI
from app.routers import auth, sessions, history
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(sessions.router)
app.include_router(history.router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Interview prep bot is running"}
