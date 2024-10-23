from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import todo, auth
from database import engine
import models


app = FastAPI()


origins = [
    "http://localhost:5173",  # Vite dev server
    "task-manager-ten-zeta.vercel.app" , #production site
    "task-manager-git-main-rhonaiyes-projects.vercel.app", #production site
    "task-manager-pvlbw8l9x-rhonaiyes-projects.vercel.app", #production site

]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


#create database
models.Base.metadata.create_all(bind=engine)


app.include_router(todo.router)
app.include_router(auth.router)