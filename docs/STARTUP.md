# 本地启动说明

本项目需要 Python 3.11、Node.js 20 或更高版本。当前仓库通过本地开发模式运行前后端；后端默认监听 8000，Vite 前端默认监听 5173。

## 1. 准备后端环境

在项目根目录执行。

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

编辑根目录的 `.env`，至少填写 `OPENAI_API_KEY`。根据模型服务商调整 `OPENAI_API_BASE` 和 `OPENAI_MODEL_NAME`。模板中的默认值指向 DashScope 的 OpenAI 兼容 API。不要提交填写后的 `.env` 文件。

## 2. 启动后端

激活虚拟环境后，在第一个终端从项目根目录运行：

~~~bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
~~~

后端启动时会初始化数据库并启动后台任务 worker。

## 3. 启动前端

在第二个终端运行：

~~~bash
cd frontend-vue
npm ci
npm run dev
~~~

使用 Vite 显示的地址打开前端，通常是 `http://127.0.0.1:5173`。开发服务器会将 API 请求代理至 `http://127.0.0.1:8000`。

## 4. 检查服务

- 前端页面：`http://127.0.0.1:5173`
- 后端健康检查：`http://127.0.0.1:8000/health`
- FastAPI 接口文档：`http://127.0.0.1:8000/docs`

## 常见问题

- 模型请求报认证错误：检查 `.env` 中的 API Key 和模型服务权限。
- 模型或接口找不到：确认 `OPENAI_API_BASE` 与 `OPENAI_MODEL_NAME` 符合服务商说明。
- 修改环境变量后未生效：停止并重新启动后端进程。
- 前端无法连接 API：确认后端已在 8000 端口运行，并检查 `frontend-vue/vite.config.ts` 中的代理配置。
