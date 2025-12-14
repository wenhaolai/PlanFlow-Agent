from fastapi import FastAPI
import os

app = FastAPI()


@app.get("/")
async def root():
    return {"message":  os.getenv("DASHSCOPE_API_KEY")}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
