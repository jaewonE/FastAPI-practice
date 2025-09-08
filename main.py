# main.py
from fastapi import FastAPI
from apis.todo import router as todo_router
from apis.user import router as user_router
from apis.ml import router as ml_router
from error.handlers import register_exception_handlers

app = FastAPI(title="Todo API", version="1.0.0")
app.include_router(todo_router)
app.include_router(user_router)
app.include_router(ml_router)

# 전역 예외 처리
register_exception_handlers(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7701)
