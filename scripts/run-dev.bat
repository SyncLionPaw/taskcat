@echo off
echo ======================================
echo SQL Practice Environment Check
echo ======================================
python src/scripts/check_docker_env.py
if %errorlevel% neq 0 (
    echo.
    echo Warning: Docker environment check failed!
    echo SQL Practice feature may not work correctly.
    echo.
    echo Press any key to continue anyway...
    pause > nul
) else (
    echo.
    echo Docker environment check passed!
    echo.
)

echo Starting API server...
uv run -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

@REM API 文档：http://localhost:8000/docs
@REM 替代文档：http://localhost:8000/redoc
@REM API 根路径：http://localhost:8000/api/v1/users