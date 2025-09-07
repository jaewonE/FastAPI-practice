# main.py
from fastapi import FastAPI
from apis.todo import router as todo_router

app = FastAPI(title="Todo API", version="1.0.0")
app.include_router(todo_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7701)
