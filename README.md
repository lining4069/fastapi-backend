# FastAPI Project Baseline

> 一个可直接复用的 **FastAPI 后端项目骨架（Baseline / Template）**，内置主流工程实践，适合作为新项目的起点。

---

## ✨ 项目简介

本项目旨在提供一个**工程化、结构清晰、可扩展**的 FastAPI 项目基础模板，已经完成并验证了以下关键能力：

* 清晰、可维护的代码组织结构
* 统一的配置管理（Pydantic Settings + `.env`）
* 标准化日志系统（stdout + 文件，支持滚动）
* API Router 分层设计（versioned API）
* SQLAlchemy ORM 示例
* Pydantic 输入 / 输出 Schema 示例
* 可直接运行、可作为新项目起点

你可以通过 **Git tag / Release** 直接 clone 或下载 ZIP，用于快速启动新项目。

---

## 📁 项目目录结构说明

```text
.
├── alembic/                # 数据库迁移（Alembic）
├── alembic.ini
├── app/
│   ├── .env                # 环境变量（开发环境示例）
│   ├── main.py             # FastAPI 应用入口
│   │
│   ├── api/                # API 层（路由层）
│   │   ├── v1/             # API 版本
│   │   │   ├── api.py      # v1 Router 聚合
│   │   │   └── endpoints/  # 具体业务路由
│   │   │       ├── news.py
│   │   │       └── users.py
│   │
│   ├── core/               # 核心基础设施（横切关注点）
│   │   ├── config.py       # 配置定义（Pydantic Settings）
│   │   ├── logging.py      # 日志系统（stdout + file）
│   │   ├── database.py     # 数据库连接 / Session 管理
│   │   └── security.py     # 安全相关（预留）
│   │
│   ├── common/             # 通用工具
│   │   ├── responses.py    # 统一响应封装
│   │   ├── pagination.py  # 分页工具
│   │   └── exceptions.py  # 自定义异常
│   │
│   ├── modules/            # 业务模块（领域层）
│   │   ├── news/
│   │   │   ├── model.py    # ORM Model
│   │   │   ├── schema.py   # Pydantic Schema（In / Out）
│   │   │   ├── repository.py # 数据访问层
│   │   │   └── service.py  # 业务逻辑层
│   │   └── users/          # 其他业务模块（示例）
│   │
│   └── tests/              # 测试（预留）
│
├── requirements.txt
└── README.md
```

---

## 🧱 架构设计说明

### 分层原则

* **api 层**：

  * 仅负责 HTTP 协议、参数校验、返回结果
  * 不包含业务逻辑

* **modules 层（领域层）**：

  * `model`：数据库模型（SQLAlchemy ORM）
  * `schema`：Pydantic 输入 / 输出模型
  * `repository`：数据访问（CRUD）
  * `service`：业务逻辑聚合

* **core 层（基础设施）**：

  * 系统配置、日志、数据库、安全
  * 与业务无关，可复用

* **common 层**：

  * 通用响应、异常、分页等工具

---

## ⚙️ 已具备的功能

### ✅ 配置管理

* 使用 `pydantic-settings`
* 支持 `.env` 文件加载
* 支持环境变量覆盖
* 配置结构集中在 `app/core/config.py`

---

### ✅ 日志系统

* 基于 Python `logging` 标准库
* **双通道输出**：

  * stdout（适配 Docker / K8s）
  * 文件日志（按天滚动，保留历史）
* 统一日志格式：

```text
2026-02-09 10:32:41 | INFO     | app.api.endpoints.news:12 | Fetching news list
```

* 模块级 logger：

```python
from app.core.logging import get_logger
logger = get_logger(__name__)
```

---

### ✅ API Router 示例

* 使用 FastAPI `APIRouter`
* 支持 API 版本管理（`/api/v1`）
* 示例路由：`news`, 
* AsyncSession 依赖注入（`/api/core/database.py`）

---

### ✅ 数据库与 ORM

* SQLAlchemy ORM
* Session 管理集中在 `core/database.py`
* 业务模块通过 repository 访问数据库
* 支持 Alembic 数据库迁移

---

### ✅ Pydantic Schema（输入 / 输出）

* 输入校验（Request Schema）
* 输出序列化（Response Schema）
* 与 ORM 解耦

---

## 🚀 项目运行步骤

### 1️⃣ 克隆项目（指定版本）

```bash
git clone --branch v0.1.0 https://github.com/lining4069/fastapi-backend.git
cd fastapi-backend
```

或直接下载 GitHub Release 的 ZIP。

---

### 2️⃣ 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\\Scripts\\activate  # Windows
```

---

### 3️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

---

### 4️⃣ 配置环境变量

编辑 `app/.env`：

```env
DATABASE_USER=`user`
DATABASE_PASSWORD=`password`
DATABASE_HOST=`host`
DATABASE_PORT=`port`
DATABASE_NAME=`db`
```

---

### 5️⃣ 启动应用

```bash
uvicorn app.main:app --reload
```

访问：

* Swagger UI：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🏷 版本管理说明

* 使用 **Git tag + Semantic Versioning**
* 当前版本示例：`v0.1.0`
* 推荐 clone 指定 tag 作为新项目起点

---

## 🔮 后续可扩展方向（规划）

* JWT / OAuth2 认证
* JSON 日志（ELK / Loki）
* 多环境配置（dev / test / prod）
* 单元测试 / 集成测试
* +langchain/langgraph Agent/RAG

---

## 📄 License

MIT License（可根据需要调整）

---

> 该项目适合作为 **FastAPI 后端项目模板 / 基线工程**，用于快速启动新服务，并在此基础上持续演进。
