# 项目启动说明

本项目支持本地开发启动和 Docker 启动，两种方式任选其一。

## 启动前配置

在项目根目录复制 `.env.example` 为 `.env`，填写自己的接口服务配置：

```powershell
Copy-Item .env.example .env
```

必须填写：

```dotenv
OPENAI_API_KEY=你的密钥
OPENAI_API_BASE=你的兼容接口地址
OPENAI_MODEL_NAME=你的模型名
```

不要将 `.env` 发给他人或提交到版本库。

## 方式一：本地开发启动

需要 Conda、Python 3.11、Node.js 20 或更高版本。

```powershell
conda create -n multi_agent_v1 python=3.11 -y
conda activate multi_agent_v1
pip install -r requirements.txt

cd frontend-vue
npm ci
cd ..
```

打开两个终端窗口，在项目根目录分别执行：

```powershell
start.bat backend
```

```powershell
start.bat frontend
```

浏览器访问 `http://127.0.0.1:5173`。

## 方式二：Docker 启动

启动 Docker Desktop 后，在项目根目录执行：

```powershell
start.bat docker
```

浏览器访问：

- 页面：`http://127.0.0.1:8080`
- 接口文档：`http://127.0.0.1:8000/docs`
- 健康检查：`http://127.0.0.1:8000/health`

停止服务：

```powershell
start.bat docker-down
```
