# 模型接入配置

## 当前支持方式

当前跟踪的运行实现使用 LangChain 的 OpenAI Chat Completions 客户端，通过 OpenAI 兼容接口调用模型。它支持 OpenAI 服务以及实现兼容接口的第三方服务；仓库中没有接入独立的 Anthropic、Gemini、Azure 或 Ollama Provider。

首次启动前，在项目根目录复制 `.env.example` 为 `.env`，然后设置以下变量：

~~~dotenv
OPENAI_API_KEY=your-api-key
OPENAI_API_BASE=https://provider.example.com/v1
OPENAI_MODEL_NAME=provider-model-name
OPENAI_TIMEOUT_SECONDS=180
STRUCTURED_OUTPUT_METHOD=function_calling
~~~

| 变量 | 用途 |
| --- | --- |
| `OPENAI_API_KEY` | 模型服务认证密钥 |
| `OPENAI_API_BASE` | OpenAI 兼容 API 的 Base URL |
| `OPENAI_MODEL_NAME` | 服务商提供的模型名 |
| `OPENAI_TIMEOUT_SECONDS` | 请求超时时间，默认 180 秒 |
| `STRUCTURED_OUTPUT_METHOD` | LangChain 结构化输出方式，默认 `function_calling` |

默认模板使用 DashScope OpenAI 兼容接口和 `qwen-max`。如果改用其他服务，请按其文档填写 Base URL、模型名称和 API Key。不要提交真实的 `.env` 文件或将密钥写入源码。

## LangSmith（可选）

需要追踪模型调用时，可配置：

~~~dotenv
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key
LANGCHAIN_PROJECT=multi-agent-v1
~~~

不用 LangSmith 时保持模板中的 `LANGCHAIN_TRACING_V2=false`。

## 记忆能力

记忆检索由 `MEMORY_ENABLED` 控制，模板默认关闭。启用前请确认已配置所需模型能力和本地存储依赖。Embedding 模型名由 `MEMORY_EMBEDDING_MODEL` 提供；远程 Embedding 不可用时实现会回退至本地 Hash 向量。

其他流程开关包括 `DIALOGUE_ENABLED`、`PLAN_VARIANTS_ENABLED`、`REPAIRER_ENABLED` 和 `SELF_REFINE_ENABLED`。未显式设置的配置项会使用 `app/core/config.py` 中定义的默认值。

## 排查提示

- `401/403`：检查 Key、账号权限和服务端授权。
- `404`：检查 API Base URL 和模型名称。
- 结构化输出失败：检查服务商是否支持所选输出方法，并尝试其兼容模式。
- 修改 `.env` 后配置未变化：重启后端进程。
