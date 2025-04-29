@echo off
uv run -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

@REM API 文档：http://localhost:8000/docs
@REM 替代文档：http://localhost:8000/redoc
@REM API 根路径：http://localhost:8000/api/v1/users