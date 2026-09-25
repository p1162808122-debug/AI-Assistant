"""LLM 模型接入层 —— 统一管理 ChatOpenAI 实例。

适配 langchain-openai >= 1.1。
"""

from __future__ import annotations

from functools import lru_cache

from langchain_openai import ChatOpenAI

from app.core.config import get_settings


def _dashscope_extra_body() -> dict | None:
    settings = get_settings()
    base_url = settings.openai_api_base.lower()
    model_name = settings.openai_model_name.lower()
    thinking_model_prefixes = ("qwen3", "glm-5")
    if "dashscope" in base_url and model_name.startswith(thinking_model_prefixes):
        return {"enable_thinking": False}
    return None


@lru_cache()
def get_llm(temperature: float = 0.3) -> ChatOpenAI:
    """获取默认 LLM 实例。"""
    settings = get_settings()
    return ChatOpenAI(
        model=settings.openai_model_name,
        api_key=settings.openai_api_key,
        base_url=settings.openai_api_base,
        temperature=temperature,
        timeout=settings.openai_timeout_seconds,
        max_retries=2,
        extra_body=_dashscope_extra_body(),
    )


def get_creative_llm() -> ChatOpenAI:
    """获取用于创意/方案生成的高 temperature LLM。"""
    settings = get_settings()
    return ChatOpenAI(
        model=settings.openai_model_name,
        api_key=settings.openai_api_key,
        base_url=settings.openai_api_base,
        temperature=0.7,
        timeout=settings.openai_timeout_seconds,
        max_retries=2,
        extra_body=_dashscope_extra_body(),
    )


def get_structured_llm(schema, *, temperature: float = 0.3, method: str | None = None):
    """获取带有结构化输出的 LLM 实例。

    使用 with_structured_output 将 LLM 绑定到 Pydantic Schema，
    返回值将直接是 Pydantic 模型实例。
    """
    llm = get_llm(temperature)
    settings = get_settings()
    structured_method = method or settings.structured_output_method
    return llm.with_structured_output(schema, method=structured_method)


def get_llm_with_tools(tools: list, *, temperature: float = 0.3) -> ChatOpenAI:
    """获取绑定工具的 LLM 实例，供 tool calling 循环使用。

    qwen-max 通过 DashScope OpenAI 兼容接口支持 function calling，
    格式与 OpenAI 一致，bind_tools() 可直接使用。
    每次调用返回新的绑定实例（bind_tools 不可缓存，因为 tools 列表可变），
    但底层 ChatOpenAI 实例复用 get_llm() 的 lru_cache。
    """
    return get_llm(temperature).bind_tools(tools)
