# Python Template V2

> **Modern Python Project Template with FastAPI, uv, and Best Practices**

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

---

## 🌟 特性

- **现代项目结构**: `src/` 布局，清晰分层
- **极速依赖管理**: 使用 `uv` 替代 `pip`，快 10-100 倍
- **统一配置**: `pyproject.toml` 管理所有工具配置
- **类型安全**: 完整的类型注解 + MyPy 严格模式
- **代码质量**: Black + isort + Flake8 + Ruff
- **测试覆盖**: pytest + pytest-cov + pytest-asyncio
- **日志系统**: Loguru 结构化日志，支持 GCP Cloud Logging
- **配置管理**: YAML + 环境变量，多环境支持
- **容器化**: 多阶段 Dockerfile，非 root 用户运行
- **CI/CD**: GitHub Actions 工作流模板

---

## 📁 项目结构

```
python-template-v2/
├── .github/
│   └── workflows/              # GitHub Actions CI/CD
│       └── ci-cd.yaml
├── .vscode/                    # VSCode 配置
│   ├── launch.json
│   └── settings.json
├── src/                        # 源代码目录
│   ├── __init__.py
│   ├── configs/                # 配置模块
│   │   ├── __init__.py
│   │   ├── config.py           # 配置加载器
│   │   ├── config_local.yaml   # 本地环境配置
│   │   ├── config_dev.yaml     # 开发环境配置
│   │   ├── config_prod.yaml    # 生产环境配置
│   │   ├── log_config.py       # Loguru 日志配置
│   │   └── proxy.py            # 代理配置
│   ├── models/                 # 数据模型
│   │   ├── __init__.py
│   │   ├── requests.py         # 请求模型
│   │   └── responses.py        # 响应模型
│   ├── routers/                # API 路由
│   │   ├── __init__.py
│   │   ├── health.py           # 健康检查
│   │   └── search.py           # 搜索接口
│   ├── services/               # 业务逻辑层
│   │   ├── __init__.py
│   │   └── search_service.py
│   ├── engine/                 # 引擎层
│   │   ├── __init__.py
│   │   ├── duckdb_client.py
│   │   └── query_builder.py
│   ├── utils/                  # 工具模块
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   └── path_utils.py
│   ├── main.py                 # FastAPI 应用工厂
│   └── server.py               # 服务启动入口
├── test/                       # 测试目录
│   ├── __init__.py
│   ├── conftest.py             # pytest fixtures
│   ├── test_routers/
│   ├── test_services/
│   └── test_engine/
├── .dockerignore
├── .env-template               # 环境变量模板
├── .gitignore
├── Dockerfile
├── pyproject.toml              # 项目配置 (统一配置管理)
└── README.md
```

---

## 🚀 快速开始

### 前置要求

- Python 3.12+
- uv (推荐) 或 pip

### 安装 uv (推荐)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/nvd11/python-template-v2.git
cd python-template-v2

# 创建虚拟环境
uv venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安装所有依赖 (包括开发依赖)
uv sync --extra dev

# 或传统方式
# uv pip install -e ".[dev]"
```

### 配置环境

```bash
# 复制环境变量模板
cp .env-template .env

# 编辑 .env 文件，根据需要修改配置
vim .env
```

### 运行服务

```bash
# 方式 1: 模块方式 (推荐)
python -m src.server

# 方式 2: Uvicorn 直接启动
uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload

# 方式 3: 直接运行
python src/server.py
```

### 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🧪 运行测试

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=src --cov-report=html

# 运行特定测试文件
pytest test/test_routers/test_health.py -v

# 运行特定测试类
pytest test/test_routers/test_health.py::TestHealthRouter -v

# 运行特定测试方法
pytest test/test_routers/test_health.py::TestHealthRouter::test_health_check -v
```

---

## 🔧 代码质量

### 格式化代码

```bash
# Black 格式化
black src/ test/

# isort 导入排序
isort src/ test/
```

### 类型检查

```bash
# MyPy 类型检查
mypy src/
```

### 代码检查

```bash
# Flake8 检查
flake8 src/ test/

# Ruff 极速检查 (可选)
ruff check src/ test/
```

### 安全检查

```bash
# Bandit 安全检查
bandit -r src/
```

---

## 🐳 Docker 部署

### 构建镜像

```bash
docker build -t python-template-v2:latest .
```

### 运行容器

```bash
docker run -d \
  --name python-template-v2 \
  -p 8000:8000 \
  -e APP_ENVIRONMENT=prod \
  python-template-v2:latest
```

### Docker Compose (可选)

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - APP_ENVIRONMENT=prod
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

---

## ☸️ Kubernetes 部署

本项目使用 **ArgoCD GitOps** 模式部署，配合共享 Helm Chart。

### 1. 推送镜像到 GHCR

```bash
# 构建并推送镜像
docker build -t ghcr.io/nvd11/python-template-v2:latest .
docker push ghcr.io/nvd11/python-template-v2:latest
```

### 2. 配置 ArgoCD Application

在 `my-argocd-manifests` 仓库中创建：

```yaml
# argocd-apps/python-template-v2-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: python-template-v2
  namespace: argocd
spec:
  project: default
  sources:
    - repoURL: 'https://github.com/nvd11/my-shared-helm-charts.git'
      path: charts/generic-web-service-v2
      targetRevision: HEAD
      helm:
        valueFiles:
          - $values/infrastructure/python-template-v2/values.yaml
    - repoURL: 'https://github.com/nvd11/my-argocd-manifests.git'
      targetRevision: HEAD
      ref: values
  destination:
    name: 'tencent-dp1-cluster'
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### 3. 配置 Helm Values

```yaml
# infrastructure/python-template-v2/values.yaml
replicaCount: 1

image:
  repository: ghcr.io/nvd11/python-template-v2
  tag: latest
  pullPolicy: IfNotPresent

containerPort: 8000

env:
  - name: APP_ENVIRONMENT
    value: "prod"

resources:
  requests:
    cpu: 50m
    memory: 64Mi
  limits:
    cpu: "1"
    memory: 512Mi

livenessProbe:
  enabled: true
  path: /live
  port: http

readinessProbe:
  enabled: true
  path: /ready
  port: http

service:
  type: ClusterIP
  port: 8000
```

---

## 📝 环境变量

| 变量名 | 默认值 | 描述 |
|--------|--------|------|
| `APP_ENVIRONMENT` | `dev` | 应用环境 (local/dev/prod) |
| `APP_HOST` | `0.0.0.0` | 监听地址 |
| `APP_PORT` | `8000` | 监听端口 |
| `APP_WORKERS` | `1` | Worker 数量 |
| `APP_DEBUG` | `false` | 调试模式 |
| `APP_LOG_LEVEL` | `INFO` | 日志级别 |

---

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/)
- [uv](https://github.com/astral-sh/uv)
- [Loguru](https://github.com/Delgan/loguru)
- [Pydantic](https://docs.pydantic.dev/)

---

*由 Cindy 💕 为 Jason 精心打造*
