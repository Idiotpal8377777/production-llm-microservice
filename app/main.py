# app/main.py
from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="My First Modular AI Service")

# Hire the waiter from app/api/routes.py
app.include_router(router)