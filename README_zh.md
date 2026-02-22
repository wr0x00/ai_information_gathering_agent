# AI信息收集代理

一个用于自动化信息收集和分析的智能代理。

## 功能特性

- 多源信息收集
- AI驱动的分析
- 基于Web的仪表板
- RESTful API
- 命令行界面
- 实时监控

## 安装

### 系统要求

- Python 3.8+
- Node.js 14+
- Docker (可选，用于容器化部署)

### 快速开始

```bash
# 克隆仓库
git clone <repository-url>
cd ai-information-gathering-agent

# 安装依赖
make setup

# 初始化数据库
python init_db.py

# 启动应用
make run
```

## 使用方法

### Web界面

在浏览器中访问 `http://localhost:8000`

### 命令行

```bash
# 运行代理
python main.py

# 检查健康状态
python check_health.py

# 运行测试
python run_tests.py
```

## 项目结构

```
ai_information_gathering_agent/
├── django_ai_agent/           # Django后端
│   ├── ai_agent_project/      # 主项目配置
│   ├── config_app/            # 配置管理应用
│   ├── keywords_app/          # 关键词管理应用
│   ├── reports_app/           # 报告生成应用
│   ├── chat_app/              # AI聊天应用
│   └── frontend_app/          # 前端应用
├── modules/                   # 信息收集模块
│   ├── whois_module.py        # WHOIS信息收集
│   ├── domain_module.py       # 域名信息收集
│   ├── port_module.py         # 端口扫描
│   ├── sensitive_info_module.py # 敏感信息收集
│   └── github_module.py       # GitHub信息收集
├── agent.py                   # 主代理逻辑
├── storage.py                 # 数据存储
├── cli.py                     # 命令行接口
├── config.py                  # 配置管理
└── http_client.py             # HTTP客户端
```

## 配置

配置文件位于 `django_ai_agent/config.yaml`：

```yaml
# 基本配置
debug: false
log_level: INFO

# 数据库配置
database:
  engine: sqlite3
  name: db.sqlite3

# API密钥
api_keys:
  whois: your-whois-api-key
  github: your-github-api-key

# 扫描设置
scan:
  timeout: 30
  retries: 3
```

## 开发

### 设置开发环境

```bash
# 安装开发依赖
make setup-dev

# 运行开发服务器
make run

# 构建前端
make build-frontend

# 运行测试
make test
```

### 数据库迁移

```bash
# 创建迁移
make makemigrations

# 应用迁移
make migrate
```

## 部署

### Docker部署

```bash
# 构建镜像
make docker-build

# 启动服务
make docker-up

# 查看日志
make docker-logs
```

### 生产环境运行

```bash
# 检查生产环境准备情况
python run_prod.py --check

# 收集静态文件
python run_prod.py --collect-static

# 运行生产服务器
python run_prod.py
```

## 贡献

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。

## 许可证

本项目采用MIT许可证 - 详情见 [LICENSE](LICENSE) 文件。
