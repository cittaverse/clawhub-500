#!/usr/bin/env python3
"""
ClawHub 500 配置文件
支持阿里云百炼 API (OpenAI 兼容格式)
"""

import os

# API 配置
API_CONFIG = {
    "tavily": {
        "api_key": os.environ.get("TAVILY_API_KEY", ""),
        "base_url": "https://api.tavily.com",
    },
    "virustotal": {
        "api_key": os.environ.get("VIRUSTOTAL_API_KEY", ""),
        "base_url": "https://www.virustotal.com/api/v3",
    },
    "openai": {
        "api_key": os.environ.get("OPENAI_API_KEY", ""),
        "base_url": os.environ.get(
            "OPENAI_BASE_URL",
            "https://coding.dashscope.aliyuncs.com/v1"  # 阿里云百炼默认
        ),
        "model": os.environ.get(
            "OPENAI_MODEL",
            "qwen3-coder-plus"  # 阿里云百炼默认模型
        ),
    },
}

def get_openai_client():
    """获取 OpenAI 兼容客户端 (支持阿里云百炼)"""
    from openai import OpenAI
    
    client = OpenAI(
        api_key=API_CONFIG["openai"]["api_key"],
        base_url=API_CONFIG["openai"]["base_url"],
    )
    
    return client

def get_model_name():
    """获取当前配置的模型名称"""
    return API_CONFIG["openai"]["model"]

# 验证配置
def validate_config():
    """验证所有 API 配置"""
    errors = []
    
    if not API_CONFIG["tavily"]["api_key"]:
        errors.append("TAVILY_API_KEY 未配置")
    
    if not API_CONFIG["virustotal"]["api_key"]:
        errors.append("VIRUSTOTAL_API_KEY 未配置")
    
    if not API_CONFIG["openai"]["api_key"]:
        errors.append("OPENAI_API_KEY 未配置")
    
    if errors:
        print("❌ 配置验证失败:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print("✅ 配置验证通过")
    print(f"  - Tavily API: 已配置")
    print(f"  - VirusTotal API: 已配置")
    print(f"  - OpenAI API (百炼): {API_CONFIG['openai']['model']}")
    return True

if __name__ == "__main__":
    validate_config()
