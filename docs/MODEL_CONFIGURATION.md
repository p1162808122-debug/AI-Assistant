# 模型接入配置

## 1. 配置文件

在项目根目录将 `.env.example` 复制为 `.env`，所有模型配置均在 `.env` 中完成。交付包不包含 `.env`，认证凭据字段保持为空，使用者需填写自己的服务信息。

通用配置项：

```dotenv
LLM_PROVIDER=openai_compatible
LLM_API_KEY=
LLM_API_BASE=https://provider.example.com/v1
LLM_MODEL_NAME=provider-model-name
LLM_TIMEOUT_SECONDS=180
LLM_MAX_RETRIES=2
STRUCTURED_OUTPUT_METHOD=function_calling
```

| 配置项 | 说明 |
| --- | --- |
| `LLM_PROVIDER` | 模型服务类型 |
| `LLM_API_KEY` | 使用者自己的认证凭据，交付包内为空 |
| `LLM_API_BASE` | 模型服务接口地址 |
| `LLM_MODEL_NAME` | 服务商提供的模型名称或部署名称 |
| `LLM_TIMEOUT_SECONDS` | 单次请求超时时间 |
| `LLM_MAX_RETRIES` | 请求失败后的最大重试次数 |
| `STRUCTURED_OUTPUT_METHOD` | 结构化输出方式 |

## 2. OpenAI-compatible

适用于提供 OpenAI Chat Completions 兼容接口的模型服务。接口地址和模型名称以服务商控制台为准。

```dotenv
LLM_PROVIDER=openai_compatible
LLM_API_BASE=https://provider.example.com/v1
LLM_MODEL_NAME=provider-model-name
STRUCTURED_OUTPUT_METHOD=function_calling
```

## 3. OpenAI

```dotenv
LLM_PROVIDER=openai
LLM_API_BASE=
LLM_MODEL_NAME=gpt-4.1
STRUCTURED_OUTPUT_METHOD=function_calling
```

## 4. Azure OpenAI

`LLM_API_BASE` 填写 Azure endpoint，`LLM_MODEL_NAME` 填写 deployment name。

```dotenv
LLM_PROVIDER=azure_openai
LLM_API_BASE=https://resource-name.openai.azure.com
LLM_MODEL_NAME=deployment-name
AZURE_OPENAI_API_VERSION=2024-10-21
```

## 5. Anthropic Claude

```dotenv
LLM_PROVIDER=anthropic
LLM_API_BASE=
LLM_MODEL_NAME=claude-model-name
```

## 6. Google Gemini

```dotenv
LLM_PROVIDER=gemini
LLM_API_BASE=
LLM_MODEL_NAME=gemini-model-name
```

## 7. Ollama

本地运行时使用 Ollama 服务地址；模型需提前在 Ollama 中准备完成。

```dotenv
LLM_PROVIDER=ollama
LLM_API_BASE=http://127.0.0.1:11434
LLM_MODEL_NAME=local-model-name
```

Docker 容器访问 Windows 宿主机上的 Ollama 时，可将地址改为 `http://host.docker.internal:11434`。

## 8. 模型能力要求

| Provider | 结构化输出 | Tool Calling |
| --- | --- | --- |
| OpenAI-compatible | 取决于服务商和具体模型 | 取决于服务商和具体模型 |
| OpenAI | 支持 | 支持 |
| Azure OpenAI | 支持 | 取决于部署模型 |
| Anthropic | 支持 | 取决于具体模型 |
| Gemini | 支持 | 取决于具体模型 |
| Ollama | 取决于本地模型 | 取决于本地模型 |

核心流程要求模型能够稳定返回结构化内容。启用记忆检索功能时，所选模型还应支持 Tool Calling。

## 9. 记忆检索配置

默认关闭远程记忆增强，不影响任务主流程：

```dotenv
MEMORY_ENABLED=false
MEMORY_EMBEDDING_PROVIDER=auto
MEMORY_EMBEDDING_MODEL=text-embedding-v3
```

设置为 `auto` 时，OpenAI/OpenAI-compatible 服务会尝试使用远程 Embedding；其他 Provider 自动使用本地 Hash 方式。设置 `MEMORY_EMBEDDING_PROVIDER=hash` 可完全使用本地方式。

## 10. 常见问题

- 返回 `401/403`：检查认证凭据、账号权限和接口地址。
- 返回 `404 model not found`：检查模型名称、部署名称和接口地址。
- 结构化输出失败：确认具体模型支持结构化输出，并检查 `STRUCTURED_OUTPUT_METHOD`。
- Tool Calling 无结果：换用明确支持工具调用的模型，或保持记忆增强功能关闭。
- Ollama 无法连接：确认 Ollama 已启动，并检查本地与 Docker 环境的访问地址。
- 修改 `.env` 后配置未生效：完整重启后端服务。
