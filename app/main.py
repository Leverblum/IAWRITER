# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import users, posts
from .database import Base, engine

# crea tablas al arrancar (usa engine configurado - sqlite local por defecto)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Blog")

# Orígenes permitidos (añade tu GitHub Pages aquí)
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://TU_GITHUB_PAGES_URL.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registramos routers con prefijos claros
app.include_router(users.router)
app.include_router(posts.router)


@app.get("/")
def root():
    return {"message": "AI Blog API is running"}
