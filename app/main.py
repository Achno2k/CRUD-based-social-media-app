from fastapi import FastAPI
from .database import engine
from . import models
from .routes import posts, users, auth, votes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# models.Base.metadata.create_all(bind=engine)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router) 

origins = ["*"]    #this means all domains are allowed to access our API

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}



