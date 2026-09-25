# 多智能体需求交付系统 (Multi-Agent Delivery System)

基于 LangChain + LangGraph 的多 Agent 协作系统，将自然语言需求转化为完整的项目交付包。

## 系统概述

本系统通过多个专业智能体的协作，实现从需求输入到技术交付的全流程自动化：

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   需求输入   │ -> │  需求澄清    │ -> │  方案设计    │ -> │  工程实现    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                              │
                        ┌─────────────┐    ┌─────────────┐   │
                        │  交付打包    │ <- │  人工审批    │ <-┘
                        └─────────────┘    └─────────────┘
```

## 核心特性

- **多智能体协作**：Planner、Solution、Engineer、Reviewer 等专业 Agent 分工协作
- **人机协同**：支持人工澄清和审批节点，确保交付质量
- **状态驱动**：基于 LangGraph 的状态机工作流，支持断点续传
- **全流程交付**：输出需求澄清文档、PRD、技术设计、代码骨架和评审报告

## 技术栈

| 组件 | 技术 |
|------|------|
| 智能体框架 | LangChain + LangGraph |
| LLM 接口 | OpenAI API |
| 后端服务 | FastAPI + Uvicorn |
| 前端界面 | Vue 3 + TypeScript + Vite |
| 数据存储 | SQLite + SQLAlchemy |
| 向量存储 | ChromaDB |

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd mutil_agent_v1

# 创建虚拟环境
conda create -n multi-agent python=3.11
conda activate multi-agent

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，并填写您的配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# LLM Configuration (必填)
OPENAI_API_KEY=your-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4o

# LangSmith (可选)
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=multi-agent-v1

# Database
DATABASE_URL=sqlite+aiosqlite:///./data/tasks.db

# App
APP_ENV=development
LOG_LEVEL=INFO
MAX_REFLOW_COUNT=2
```

### 3. 启动服务（任选一种）

**方式一：本地开发启动（适合调试、截图和二次开发）**

```bash
# 终端 1：启动 FastAPI 后端
start.bat backend

# 终端 2：启动 Vue 前端
start.bat frontend
```

前端地址：`http://127.0.0.1:5173`。

**方式二：Docker 启动（适合环境隔离和快速部署）**

```bash
start.bat docker
```

前端地址：`http://127.0.0.1:8080`。

详细准备步骤与故障排查见 [安装部署指南](docs/安装部署指南.md)。

### 4. 访问系统

- **本地开发前端**：http://localhost:5173
- **Docker 前端**：http://localhost:8080
- **API 文档**：http://localhost:8000/docs
- **健康检查**：http://localhost:8000/health

## 项目结构

```
mutil_agent_v1/
├── app/
│   ├── agents/           # 智能体实现
│   │   ├── orchestrator_agent.py   # 编排器：输入规范化、人工交互、打包
│   │   ├── planner_agent.py        # 规划器：需求澄清与结构化
│   │   ├── solution_agent.py       # 方案师：PRD 与技术方案
│   │   ├── engineer_agent.py       # 工程师：代码骨架生成
│   │   └── reviewer_agent.py       # 评审员：质量检查
│   ├── api/              # API 路由
│   │   └── routes_task.py          # 任务管理接口
│   ├── core/             # 核心组件
│   │   ├── config.py               # 配置管理
│   │   ├── llm.py                  # LLM 封装
│   │   ├── logger.py               # 日志配置
│   │   └── prompts.py              # Prompt 模板
│   ├── graph/            # 工作流图
│   │   ├── builder.py              # 图构建器
│   │   ├── checkpoints.py          # 状态检查点
│   │   ├── router.py               # 路由逻辑
│   │   └── state.py                # 状态定义
│   ├── schemas/          # 数据模型
│   ├── storage/          # 数据存储
│   ├── tools/            # 工具函数
│   └── main.py           # FastAPI 入口
├── frontend-vue/         # Vue 前端
├── data/                 # 数据目录
├── output/               # 交付物输出目录
├── tests/                # 测试用例
├── requirements.txt      # 依赖列表
└── start.bat             # Windows 启动脚本
```

## 工作流说明

系统采用 LangGraph 构建的工作流，包含以下节点：

| 节点 | 职责 | 说明 |
|------|------|------|
| input_normalize | 输入规范化 | 清理和标准化用户输入 |
| planner | 需求规划 | 分析需求，识别待澄清问题 |
| human_clarification | 人工澄清 | 需求不明确时暂停等待用户补充 |
| solution | 方案设计 | 生成 PRD 和技术设计方案 |
| engineer | 工程实现 | 生成代码骨架和项目结构 |
| reviewer | 质量评审 | 检查交付物质量，决定是否回流 |
| human_approval | 人工审批 | 人工确认后进入打包阶段 |
| package_output | 交付打包 | 汇总所有产物生成最终交付包 |

### 回流机制

当 Reviewer 发现质量问题时，系统支持回流到上游节点重新处理：

- **最大回流次数**：可通过 `MAX_REFLOW_COUNT` 配置（默认 2 次）
- **回流目标**：根据问题类型回流到 Solution 或 Engineer 节点

## API 接口

### 创建任务

```bash
POST /tasks
Content-Type: application/json

{
  "user_input": "我想开发一个在线教育平台..."
}
```

### 查询任务状态

```bash
GET /tasks/{task_id}
```

### 提交人工反馈

```bash
POST /tasks/{task_id}/feedback
Content-Type: application/json

{
  "feedback": "补充信息...",
  "approved": true
}
```

### 获取交付结果

```bash
GET /tasks/{task_id}/result
```

## 交付物说明

任务完成后，系统会在 `output/{task_id}/` 目录下生成以下交付物：

| 文件 | 说明 |
|------|------|
| `requirement_*.json` | 结构化需求文档 |
| `prd_*.md` | 产品需求文档 (PRD) |
| `technical_design_*.md` | 技术设计方案 |
| `review_report_*.md` | 评审报告 |
| `full_deliverable_*.json` | 完整交付包（JSON 格式） |

## 开发指南

### 运行测试

```bash
pytest tests/ -v
```

### 代码规范

- 使用 Python 3.11+
- 遵循 PEP 8 规范
- 类型注解：使用 `from __future__ import annotations`

## 许可证

当前发布包未授予开源、商业或独家授权。发布者须先确认全部源码与素材的权属，再由实际权利人替换 [授权与权属说明](LICENSE.md) 为适用的许可证或订单授权条款。详情见 [授权与销售说明](docs/授权与销售说明.md)。

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request
