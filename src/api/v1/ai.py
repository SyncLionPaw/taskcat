from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
import httpx
import os
from pydantic import BaseModel

from src.core.auth import get_current_user
from src.models.user import User

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000
    api_key: Optional[str] = None
    api_base_url: Optional[str] = None

@router.post("/")
async def proxy_chat_request(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    代理AI聊天请求到外部API服务，避免CORS问题
    """
    print("#######", request.api_base_url, request.api_key, request.model)
    try:
        # 获取API密钥：优先使用请求中提供的，如果没有则使用环境变量
        api_key = request.api_key or os.environ.get("OPENAI_API_KEY", "")
        
        if not api_key:
            raise HTTPException(status_code=400, detail="API Key未提供")

        # 获取基本URL，默认为OpenAI
        api_base_url = request.api_base_url or "https://api.openai.com/v1/chat/completions"
        
        # 准备发送到外部API的请求主体
        payload = {
            "model": request.model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in request.messages],
        }
        
        # 添加可选参数
        if request.temperature is not None:
            payload["temperature"] = request.temperature
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens
        
        # 打印请求信息（隐藏部分API Key）
        masked_api_key = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else "***"
        print(f"发送请求到: {api_base_url}")
        print(f"API Key (已隐藏): {masked_api_key}")
        
        # 使用httpx发送请求到外部API
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            response = await client.post(
                api_base_url,
                json=payload,
                headers=headers
            )
            
            # 获取响应内容
            response_data = response.json()
            
            # 检查是否成功
            if response.status_code != 200:
                error_message = response_data.get("error", {}).get("message", "未知错误")
                print(f"API错误 ({response.status_code}): {error_message}")
                raise HTTPException(status_code=response.status_code, detail=error_message)
            
            return response_data
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="API请求超时")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"请求失败: {str(e)}")
    except Exception as e:
        print("##### 500,", str(e))
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")