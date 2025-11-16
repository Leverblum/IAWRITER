# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import users, posts
from .database import Base, engine

# crea tablas al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Blog")

# --- CORS GLOBAL (acepta peticiones desde cualquier sitio) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # <--- permitir todo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users.router)
app.include_router(posts.router)

@app.get("/")
def root():
    return {"message": "AI Blog API is running"}
