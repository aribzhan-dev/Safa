from fastapi import FastAPI
import uvicorn



app = FastAPI()
@app.get("api/")
async def root():
    return {"message": "FastAPI is working!"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=3489)