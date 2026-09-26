# 多智能体需求交付系统

一个用于把自然语言需求整理成产品与技术交付物的全栈示例项目。用户提交需求后，后端通过 LangGraph 组织多个 Agent 完成需求分析、方案生成、工程设计和质量评审；遇到信息缺口或需要确认时，由用户补充或审批。Vue 前端负责任务创建、进度查看和结果浏览。

> 当前项目适合源码学习、演示和二次开发。模型生成内容需要人工核对。当前版本通过 OpenAI 兼容接口连接模型；请先查看 [模型配置](docs/MODEL_CONFIGURATION.md)。

## 项目能做什么

- 创建需求任务，并在后台运行工作流。
- 通过人工澄清补充缺失信息，审批或驳回交付结果。
- 生成结构化需求、PRD、技术设计、代码骨架建议和评审报告。
- 对评审问题进行修复或回到相关步骤重新生成。
- 查看任务历史、实时进度和任务结果，并导出完整交付数据。

## 工作流程

浏览器 → FastAPI API / 后台任务队列 → LangGraph 工作流 → 需求规划与评估 → PRD 和技术设计 → 质量评审与修复/回流 → 人工审批 → Markdown / JSON 交付物

1. Planner 解析需求并识别需要补充的信息；Plan Evaluator 决定继续还是进入人工澄清。
2. Solution 生成 PRD，Engineer 生成技术设计和代码骨架建议。
3. Reviewer 检查交付内容；需要修改时由 Repairer 修复，或按问题类型回到方案/工程步骤。
4. 系统等待人工审批。审批通过后导出交付物；用户反馈会从持久化工作流检查点恢复执行。

## 技术组成

| 部分 | 技术与职责 |
| --- | --- |
| 前端 | Vue 3、TypeScript、Vite；创建任务、历史、进度和交付物页面 |
| API | FastAPI；任务创建、查询、反馈、结果和 SSE 进度流 |
| 工作流 | LangGraph；Agent 节点、状态传递、人工中断、评审回流和恢复 |
| 模型 | LangChain OpenAI 接口；连接 OpenAI 兼容服务 |
| 持久化 | SQLite、SQLAlchemy、LangGraph SQLite checkpoint；任务及中断状态 |
| 检索记忆 | ChromaDB；可选记忆能力，默认关闭 |

## 目录导航

| 路径 | 内容 | 建议何时阅读 |
| --- | --- | --- |
| <code>app/main.py</code> | FastAPI 应用入口、数据库初始化和后台 worker 生命周期 | 从这里了解后端如何启动 |
| <code>app/api/</code> | 任务 REST API 和 SSE 进度流 | 查找前后端接口 |
| <code>app/graph/</code> | 工作流状态、节点构建、路由和 checkpoint | 理解完整执行顺序 |
| <code>app/agents/</code> | Planner、Solution、Engineer、Reviewer 等 Agent | 查看每一步如何生成内容 |
| <code>app/schemas/</code> | 需求、PRD、技术设计和评审的数据模型 | 查找结构化输入与输出 |
| <code>app/core/</code> | 环境配置、模型接入、提示词、任务队列和日志 | 修改模型或运行配置 |
| <code>app/storage/</code>、<code>app/tools/</code> | 数据访问、记忆存储、工具和结果导出 | 追踪数据如何保存与导出 |
| <code>frontend-vue/src/</code> | 页面、组件、API composable、SSE 和状态管理 | 理解浏览器端流程 |
| <code>docs/</code> | 架构、启动、模型配置、使用及技术设计说明 | 按主题深入阅读 |

## 本地启动

需要 Python 3.11、Node.js 20 或更高版本。以下命令在项目根目录执行；前后端分别运行在两个终端。

### 1. 配置后端

macOS / Linux：

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
~~~

Windows PowerShell：

~~~powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
~~~

编辑根目录的 <code>.env</code>，填写模型服务的 <code>OPENAI_API_KEY</code>；按服务商要求设置 <code>OPENAI_API_BASE</code> 和 <code>OPENAI_MODEL_NAME</code>。默认示例使用 DashScope 的 OpenAI 兼容接口。不要把真实密钥提交到 Git。

在第一个终端启动后端：

~~~bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
~~~

### 2. 启动前端

在第二个终端，从项目根目录执行：

~~~bash
cd frontend-vue
npm ci
npm run dev
~~~

打开 Vite 输出的本地地址（通常为 <code>http://127.0.0.1:5173</code>）。前端开发服务器会将 API 请求代理到本地 FastAPI 服务。

## 常用地址与接口

- 前端：<code>http://127.0.0.1:5173</code>
- 后端健康检查：<code>http://127.0.0.1:8000/health</code>
- FastAPI 接口文档：<code>http://127.0.0.1:8000/docs</code>
- 任务接口：<code>POST /tasks</code> 创建、<code>GET /tasks</code> 列表、<code>GET /tasks/{task_id}</code> 查询
- 人工反馈：<code>POST /tasks/{task_id}/feedback</code>
- 已完成任务结果：<code>GET /tasks/{task_id}/result</code>
- 实时进度：由 SSE 路由提供，具体路径见 <code>app/api/routes_stream.py</code>

## 配置、数据与交付结果

- <code>.env.example</code> 是配置模板；本机真实配置保存在忽略文件 <code>.env</code> 中。
- SQLite 任务数据、LangGraph checkpoint、可选记忆数据位于 <code>data/</code>。
- 每个任务导出的文件位于 <code>output/{task_id}/</code>，并可通过结果 API 获取完整 JSON 数据。
- 默认关闭长期记忆；相关配置与当前支持的模型接口见 [模型配置说明](docs/MODEL_CONFIGURATION.md)。

## 文档阅读顺序

1. [启动说明](docs/STARTUP.md)：安装依赖和启动服务。
2. [项目架构](docs/PROJECT_ARCHITECTURE.md)：模块边界、数据流和部署结构。
3. [总体设计](docs/SYSTEM_DESIGN.md)：工作流、状态和扩展点。
4. [模型配置](docs/MODEL_CONFIGURATION.md)：环境变量与模型服务设置。
5. [使用说明](docs/USAGE.md)：页面操作和交付结果。
6. [技术方案](docs/TECHNICAL_SOLUTION.md)：设计细节。
