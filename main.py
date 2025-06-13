# Comando para levantar el server local: uvicorn main:app --reload
from fastapi import FastAPI
from routers import auth, users, public, appoiments, admin

app = FastAPI(
    title="Medical Appoiments",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(public.router)
app.include_router(appoiments.router)
app.include_router(admin.router)
