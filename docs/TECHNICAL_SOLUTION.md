# 技术方案文档

## 1. 建设目标

系统用于把自然语言需求转化为可审阅的需求澄清结果、PRD、技术设计、评审报告和完整 JSON 交付物。方案重点解决流程可追踪、输出结构化、模型可替换、结果可恢复以及前后端可独立二开的问题。

## 2. 技术选型

| 领域 | 选型 | 选择理由 |
| --- | --- | --- |
| Web 前端 | Vue 3、TypeScript、Vite、Pinia、Element Plus | 组件生态成熟，开发反馈快，适合管理台类产品 |
| API 服务 | FastAPI、Pydantic、Uvicorn | 类型约束清晰，自动生成 OpenAPI，异步接口实现简洁 |
| 工作流 | LangChain、LangGraph | 支持状态图、条件路由、人工中断和检查点恢复 |
| 模型接入 | LangChain ChatModel Provider Factory | 业务层与厂商 SDK 解耦，统一结构化输出和工具绑定 |
| 数据存储 | SQLite、SQLAlchemy Async | 零服务依赖，适合学习项目、演示与单机交付 |
| 记忆检索 | ChromaDB + 本地 Hash 降级 | 可选语义检索；远程 embedding 不可用时仍能运行 |
| 实时进度 | SSE | 服务端单向推送实现简单，适合长任务进度通知 |
| 部署 | 本地开发 + Docker Compose | 同时覆盖调试、截图、学习和快速部署场景 |

## 3. 模型兼容方案

模型层以 `LLM_PROVIDER` 为入口，由 `app/core/llm.py` 创建统一的 LangChain `BaseChatModel`。当前支持：

- `openai_compatible`：DashScope/Qwen、DeepSeek、Moonshot、智谱兼容模式、硅基流动、OpenRouter 等 Chat Completions 兼容服务。
- `openai`：OpenAI 官方接口。
- `azure_openai`：Azure endpoint + deployment + API version。
- `anthropic`：Claude 原生接口。
- `gemini`：Google Gemini 原生接口。
- `ollama`：本地 Ollama 服务。

结构化输出对 OpenAI 系列使用 `function_calling/json_schema` 方法，其他 Provider 使用相应 LangChain 适配器提供的结构化输出实现。

需要注意：接口兼容不等于模型能力一致。所选模型应具备稳定的结构化输出能力；启用 Engineer/Reviewer 工具循环时，还应支持 tool calling。

## 4. 异步任务方案

`POST /tasks` 只负责校验、落库和入队，快速返回任务 ID。后台 worker 执行耗时的模型工作流，避免 HTTP 请求长期占用。前端通过任务查询接口获取完整状态，通过 SSE 接收节点进度和结束事件。

该队列为进程内实现，适合单实例运行。若用于多实例或生产高并发，可将队列替换为 Redis + Celery/RQ，并保持 API 和工作流接口不变。

## 5. 质量控制方案

- Pydantic Schema 对需求、PRD、技术设计和评审结果进行字段级约束。
- Reviewer 结合规则指标与模型判断输出评分、问题和回流目标。
- `MAX_REFLOW_COUNT` 限制自动返工次数，防止无限循环和费用失控。
- Repairer 对可修复问题进行轻量修补，复杂问题回流到 Solution 或 Engineer。
- Human-in-the-loop 在澄清与最终审批阶段保留人工决策权。
- Checkpoint 保存节点状态，支持服务重启后继续等待人工处理。

## 6. 数据安全方案

- 密钥仅放置于本地 `.env`，发布包只提供 `.env.example`。
- 发布脚本排除 `.env`、数据库、日志、输出目录、IDE 配置和 Git 元数据。
- 默认使用本地 SQLite，不主动上传业务数据库。
- 调用云模型时，用户输入会发送至所选模型服务商；使用者应自行评估服务商的数据政策。
- 对外部署时建议增加登录鉴权、HTTPS、请求限流、敏感信息脱敏和密钥托管。

## 7. 性能与容量边界

当前版本面向个人学习、演示和二开起点：单进程 worker 会顺序处理任务，SQLite 适合轻量并发。影响执行时长的主要因素是模型响应速度、工作流回流次数和输入长度。生产化扩展建议包括多 worker 队列、PostgreSQL、Redis、对象存储、统一日志和监控告警。

## 8. 验收建议

1. 使用目标 provider 完成一次最小模型调用。
2. 创建任务并观察 SSE 进度。
3. 完成人工澄清或审批。
4. 检查历史任务、任务详情和导出文件。
5. 更换第二种 provider 重复测试，确认配置切换无需修改业务代码。
