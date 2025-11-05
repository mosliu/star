# 星星存折 (Star Savings)

面向3-10岁儿童的家庭奖励系统，通过星星积分激励良好行为。

## 技术栈

### 后端
- FastAPI (Python 3.11+)
- SQLite 数据库
- SQLAlchemy ORM
- RESTful API

### 前端
- Vue 3.5.18
- Vite 7.0
- TypeScript
- Tailwind CSS 4.0
- Anime.js 4.2.2

### 部署
- Docker Compose

## 核心功能

- ✅ 小朋友管理（添加、编辑、查看）
- ✅ 星星加减操作 + 可爱动画
- ✅ 星星记录查看（最近20条）
- ✅ 奖品创建（支持绑定多个小朋友）
- ✅ 奖品进度展示（星星堆叠）
- ✅ 灵活兑换（可编辑扣除分配）
- ✅ 兑换动画（烟花+翻转）
- ✅ 响应式适配（iPad/手机）

## 快速开始

### 使用 Docker Compose（推荐）

```bash
# 启动服务
docker-compose up -d

# 访问应用
# 前端: http://localhost:5173
# 后端API: http://localhost:8000/api
```

### 本地开发

#### 后端
```bash
cd python_backend
# 安装依赖
pip install -r requirements.txt
# 初始化数据库
python init_db.py
# 启动服务
python main.py
# 或使用 uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端
```bash
cd frontend
npm install
npm run dev
```

## 项目结构

```
star/
├── python_backend/   # FastAPI Python后端
│   ├── app/
│   │   ├── api/     # API端点
│   │   ├── models/  # 数据库模型
│   │   ├── schemas/ # Pydantic模式
│   │   └── core/    # 核心配置
│   ├── database.db  # SQLite数据库
│   └── main.py      # 应用入口
├── frontend/         # Vue前端
│   ├── src/
│   └── public/
├── docker-compose.yml
├── Dockerfile
├── nginx.conf
└── README.md
```

## 数据库设计

### children（小朋友表）
- 基本信息：姓名、生日、性别、头像
- star_count：当前星星总数（冗余字段）

### star_records（星星记录表）
- 记录所有加减星操作
- type: add | subtract | redeem
- reward_id: 兑换时关联奖品ID

### rewards（奖品表）
- 奖品信息：名称、图片、所需星星数
- 兑换状态

### reward_children（奖品-小朋友关联表）
- 多对多关系
- deduction_amount: 兑换时实际扣除数量

## 开发说明

### 事务处理
所有涉及星星变动的操作都使用事务保证数据一致性：
- 插入 star_records
- 更新 children.star_count

### 图标化设计
- 操作按钮：只用图标（✓×➕➖👁️）
- 少文字多图标，适合不识字的小朋友

### 动画效果
- 加星：星星飞入 + 数字跳动
- 减星：星星飞出消失
- 兑换：烟花 + 五彩纸屑

## License

MIT
