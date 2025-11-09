# 星星存折 - 项目文档

欢迎查阅星星存折（Star Savings）项目文档。本文档集合包含了项目的完整技术文档、部署指南和开发规范。

## 📚 文档目录

### 项目概述
- [项目功能概述](./项目功能概述.md) - 了解系统的整体架构和核心功能模块

### 技术文档
- [前端功能文档](./前端功能文档.md) - Vue 3前端的详细技术实现和组件说明
- [后端功能文档](./后端功能文档.md) - FastAPI后端的架构设计和功能实现
- [API接口文档](./API接口文档.md) - 完整的RESTful API接口说明和示例
- [数据库设计文档](./数据库设计文档.md) - 数据库表结构、关系和优化策略

### 部署与运维
- [部署指南](./部署指南.md) - Docker部署、手动部署、性能优化和故障排查

## 🚀 快速开始

### 本地开发
1. 克隆项目仓库
2. 安装依赖（Python 3.11+, Node.js 18+）
3. 配置环境变量
4. 启动后端服务和前端开发服务器

### Docker部署
```bash
docker-compose up -d
```

访问地址：
- 前端：http://localhost:5173
- 后端API：http://localhost:8000/api
- API文档：http://localhost:8000/docs

## 🏗️ 系统架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   前端应用   │────▶│   后端API   │────▶│   数据库    │
│   Vue 3     │     │   FastAPI   │     │  MySQL/     │
│  TypeScript │     │   Python    │     │   SQLite    │
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │                    │
       └────────────────────┴────────────────────┘
                     Docker Compose
```

## 📋 功能模块

| 模块 | 说明 | 文档链接 |
|-----|------|---------|
| 小朋友管理 | 添加、编辑、删除小朋友信息 | [查看详情](./项目功能概述.md#1-小朋友管理模块) |
| 星星系统 | 星星的增加、减少和记录查询 | [查看详情](./项目功能概述.md#2-星星积分系统) |
| 奖品管理 | 创建奖品、设置兑换条件 | [查看详情](./项目功能概述.md#3-奖品管理系统) |
| 兑换功能 | 灵活的奖品兑换和星星分配 | [查看详情](./项目功能概述.md#4-兑换系统) |

## 🛠️ 技术栈

### 前端
- Vue 3.5.18 (Composition API)
- TypeScript
- Vite 7.0
- Tailwind CSS 4.0
- Anime.js 4.2.2

### 后端
- FastAPI
- Python 3.11+
- SQLAlchemy 2.0
- Pydantic
- Alembic

### 基础设施
- Docker & Docker Compose
- Nginx
- MySQL 8.0 / SQLite 3.35

## 📊 数据库设计

主要数据表：
- `children` - 小朋友信息表
- `star_records` - 星星变动记录表
- `rewards` - 奖品信息表
- `reward_children` - 奖品与小朋友关联表

详细设计请参考[数据库设计文档](./数据库设计文档.md)

## 🔌 API接口

### 核心接口分类
1. **小朋友管理** - `/api/children`
2. **星星操作** - `/api/children/{id}/stars`
3. **奖品管理** - `/api/rewards`
4. **兑换操作** - `/api/rewards/{id}/redeem`

完整接口说明请查看[API接口文档](./API接口文档.md)

## 🎯 开发规范

### 代码规范
- Python: 遵循PEP 8规范
- TypeScript: 使用ESLint + Prettier
- Git: 采用Conventional Commits规范

### 分支策略
- `master` - 主分支，生产环境代码
- `develop` - 开发分支
- `feature/*` - 功能分支
- `hotfix/*` - 紧急修复分支

## 📈 性能优化

- 数据库查询优化（索引、连接池）
- 前端资源优化（代码分割、懒加载）
- 缓存策略（Redis、CDN）
- 负载均衡配置

## 🔒 安全措施

- HTTPS加密传输
- SQL注入防护
- XSS攻击防护
- 文件上传验证
- 定期备份策略

## 🚧 后续规划

### 近期计划
- [ ] 用户认证系统
- [ ] 任务管理模块
- [ ] 成就徽章系统
- [ ] 数据统计图表

### 长期规划
- [ ] 移动端应用
- [ ] 微服务架构
- [ ] AI智能推荐
- [ ] 多语言支持

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- Issue: [GitHub Issues](https://github.com/your-org/star-savings/issues)
- Email: support@star-savings.com

## 📄 许可证

本项目采用MIT许可证，详见[LICENSE](../LICENSE)文件。

---

最后更新时间：2024-01-03
