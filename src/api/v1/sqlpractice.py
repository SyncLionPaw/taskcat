from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
import docker
import time

from src.core.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.services.sql_practice import SQLPracticeService

router = APIRouter()
sql_practice_service = SQLPracticeService()

@router.get("/database")
async def get_current_database(
    current_user: User = Depends(get_current_user),
):
    """获取当前用户的数据库实例信息"""
    try:
        db_info = await sql_practice_service.get_user_database(current_user.id)
        return db_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/database")
async def create_database(
    options: Dict[str, Any],
    current_user: User = Depends(get_current_user),
):
    """为当前用户创建新的SQL练习数据库实例"""
    try:
        difficulty = options.get("difficulty", "easy")
        if difficulty not in ["easy", "medium", "hard"]:
            raise HTTPException(status_code=400, detail="无效的难度级别")
        
        # Get the username from options or use the current user's username
        username = options.get("username", current_user.username)
        
        # 先清理现有实例
        await sql_practice_service.cleanup_user_databases(current_user.id)
        
        # 创建新实例
        db_info = await sql_practice_service.create_database(
            user_id=current_user.id,
            username=username,
            difficulty=difficulty
        )
        return db_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/database/{database_id}")
async def get_database_info(
    database_id: str = Path(...),
    current_user: User = Depends(get_current_user),
):
    """获取特定数据库实例的信息"""
    try:
        db_info = await sql_practice_service.get_database_info(database_id)
        if not db_info:
            raise HTTPException(status_code=404, detail="数据库实例不存在")
        
        # 验证用户权限
        if str(db_info.get("user_id")) != str(current_user.id):
            raise HTTPException(status_code=403, detail="无权访问此数据库实例")
        
        return db_info
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/database/{database_id}/reset")
async def reset_database(
    database_id: str = Path(...),
    current_user: User = Depends(get_current_user),
):
    """重置数据库到初始状态"""
    try:
        # 验证用户权限
        db_info = await sql_practice_service.get_database_info(database_id)
        if not db_info:
            raise HTTPException(status_code=404, detail="数据库实例不存在")
        
        if str(db_info.get("user_id")) != str(current_user.id):
            raise HTTPException(status_code=403, detail="无权访问此数据库实例")
        
        # 执行重置
        result = await sql_practice_service.reset_database(
            database_id=database_id,
            difficulty=db_info.get("difficulty", "easy")
        )
        return {"success": True, "message": "数据库已成功重置"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/database/{database_id}/query")
async def execute_query(
    query_data: Dict[str, Any],
    database_id: str = Path(...),
    current_user: User = Depends(get_current_user),
):
    """在指定数据库中执行SQL查询"""
    try:
        # 验证用户权限
        db_info = await sql_practice_service.get_database_info(database_id)
        if not db_info:
            raise HTTPException(status_code=404, detail="数据库实例不存在")
        
        if str(db_info.get("user_id")) != str(current_user.id):
            raise HTTPException(status_code=403, detail="无权访问此数据库实例")
        
        # 获取查询参数
        sql = query_data.get("sql")
        if not sql:
            raise HTTPException(status_code=400, detail="查询参数不能为空")
        
        question_id = query_data.get("questionId")
        difficulty = query_data.get("difficulty", "easy")
        
        # 执行查询
        result = await sql_practice_service.execute_query(
            database_id=database_id,
            sql=sql,
            question_id=question_id,
            difficulty=difficulty
        )
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})

@router.delete("/database/{database_id}")
async def delete_database(
    database_id: str = Path(...),
    current_user: User = Depends(get_current_user),
):
    """删除数据库实例"""
    try:
        # 验证用户权限
        db_info = await sql_practice_service.get_database_info(database_id)
        if not db_info:
            raise HTTPException(status_code=404, detail="数据库实例不存在")
        
        if str(db_info.get("user_id")) != str(current_user.id):
            raise HTTPException(status_code=403, detail="无权访问此数据库实例")
        
        # 执行删除
        await sql_practice_service.delete_database(database_id)
        return {"success": True, "message": "数据库实例已成功删除"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
