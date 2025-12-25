# 🤖 PlanFlow-Agent 智能体系统

> **基于 Planner–Executor–Replanner 的多步骤推理智能体框架**
> 面向复杂任务的可解释、可扩展 AI Agent 架构实现

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![LLM](https://img.shields.io/badge/LLM-Qwen%20/%20OpenAI-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Ready-teal?logo=fastapi)
![Vue](https://img.shields.io/badge/Vue-3.5-blue?logo=vue.js)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?logo=mysql)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)

</div>

## 📖 项目简介

PlanFlow Agent 是一个基于 AI 的智能任务规划与执行系统。它结合了强大的后端 Agent 逻辑与现代化的前端交互界面，能够理解用户意图，拆解任务步骤，并调用工具自动执行。

## ✨ 功能特性

- **智能 Agent**: 基于 LLM 的规划 (Planner) 与执行 (Executor) 架构，支持复杂任务的自动拆解与执行。
- **对话交互**: 提供直观的聊天界面，与 Agent 进行实时交互。
- **任务管理**: 支持任务的创建、跟踪与历史记录查看。
- **用户系统**: 完整的用户注册、登录与认证流程 (JWT)。
- **现代化架构**: 前后端分离，容器化部署，易于扩展与维护。

## 🛠 技术栈

### Backend (后端)
- **框架**: [FastAPI](https://fastapi.tiangolo.com/) - 高性能 Python Web 框架
- **语言**: Python 3.10+
- **数据库 ORM**: SQLAlchemy
- **AI & LLM**: OpenAI API, LangChain (概念实现), ChromaDB (向量存储)
- **工具库**: Pydantic, PyJWT, python-multipart

### Frontend (前端)
- **框架**: [Vue 3](https://vuejs.org/)
- **构建工具**: Vite
- **UI 组件库**: Element Plus
- **样式**: Tailwind CSS
- **状态管理**: Pinia
- **路由**: Vue Router

### Database & DevOps
- **数据库**: MySQL 8.0
- **容器化**: Docker, Docker Compose
- **Web 服务器**: Nginx (前端部署)

## 📂 项目结构

```text
PlanFlow Agent/
├── backend/                # 后端代码
│   ├── agent/              # Agent 核心逻辑 (Planner, Executor, Tools)
│   ├── api/                # API 路由 (Chat, User, Tasks)
│   ├── core/               # 核心配置 (Config, Database, Security)
│   ├── models/             # 数据库模型 (SQLAlchemy Models)
│   ├── schemas/            # Pydantic 数据验证模式
│   ├── services/           # 业务逻辑层
│   ├── main.py             # 程序入口
│   └── requirements.txt    # Python 依赖
├── frontend/               # 前端代码
│   ├── src/                # Vue 源代码 (Views, Components, Stores)
│   ├── public/             # 静态资源
│   └── vite.config.js      # Vite 配置
├── database/               # 数据库脚本
│   └── init/               # 初始化 SQL 文件
└── planflow_deploy/        # 部署配置
    └── docker-compose.yml  # 容器编排文件
```


## 🧠 Plan-and-Execute 架构概览

```
用户问题
   ↓
┌───────────┐
│  Planner  │  ← 生成初始 Plan（Step List）
└─────┬─────┘
      ↓
┌───────────┐
│ Executor  │  ← 执行当前 Step（工具 / LLM）
└─────┬─────┘
      ↓
┌───────────┐
│ Replanner │  ← 根据执行结果调整 Plan
└─────┬─────┘
      ↓
 是否完成？
   ├─ 否 → Executor
   └─ 是 → 返回最终答案
```



## 🛣️ 后续扩展方向

* 多 Agent 协作（Planner Agent / Executor Agent）
* Workflow DAG 执行
* 可视化 Plan 执行过程
* 与 RAG / 知识库结合
* 与 Coze / AutoGPT 对比实验


## 🚀 快速开始

**前置要求**
- Docker & Docker Compose
- Python 3.10+ (仅本地开发后端需要)
- Node.js 20+ (仅本地开发前端需要)

1. **进入部署目录**
   ```bash
   cd planflow_deploy
   ```

2. **配置环境变量**
   在 planflow_deploy 目录下创建一个 `.env` 文件，并填入必要的配置（参考 docker-compose.yml 中的变量）：
   ```bash
   cp .env.example .env
   vim .env 
   # 修改 DASHSCOPE_API_KEY 和 SECURITY_KEY 配置
   ```

3. **启动服务**
   ```bash
   docker-compose up -d --build
   ```

4. **访问应用**
   - 前端页面: `http://localhost` (取决于 Nginx 配置端口)
   - 后端 API 文档: `http://localhost:8000/docs`
   - phpMyAdmin: `http://localhost:8080`


## 🧾 效果展示

目前仅编写了一个网络搜索工具，可以根据用户的问题进行网络搜索，并进行整合回答。

![alt text](/imgs/image.png)

![alt text](/imgs/chat.png)

## 🛣️ 后续扩展方向

* 多 Agent 协作（Planner Agent / Executor Agent）优化
* 完善可调用的Function Calling函数库
* 可视化 Plan 执行过程
* 与 RAG / 知识库结合
