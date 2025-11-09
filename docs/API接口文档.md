# API接口文档

## 基础信息

### 服务地址
- 开发环境: `http://localhost:8000/api`
- 生产环境: `https://api.star-savings.com/api`

### 认证方式
当前版本暂无认证要求，后续版本将添加JWT认证

### 请求格式
- Content-Type: `application/json`
- 字符编码: `UTF-8`

### 响应格式
所有接口统一返回JSON格式数据

#### 成功响应
```json
{
    "data": {},  // 业务数据
    "message": "Success",
    "status_code": 200
}
```

#### 错误响应
```json
{
    "error": "Error message",
    "status_code": 400,
    "timestamp": "2024-01-01T00:00:00Z"
}
```

### 状态码说明
| 状态码 | 说明 |
|-------|-----|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 422 | 数据验证失败 |
| 500 | 服务器内部错误 |

## 认证接口

### 1. 家长登录

#### 接口地址
`POST /api/auth/login`

#### 请求体
```json
{
    "username": "parent@example.com",
    "password": "password123"
}
```

#### 响应示例
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
        "id": 1,
        "username": "parent@example.com",
        "role": "parent",
        "children": [
            {"id": 1, "name": "小明"},
            {"id": 2, "name": "小红"}
        ]
    }
}
```

### 2. 儿童登录

#### 接口地址
`POST /api/auth/child-login`

#### 请求体
```json
{
    "child_id": 1,
    "pin": "1234"
}
```

#### 响应示例
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "child": {
        "id": 1,
        "name": "小明",
        "avatar": "/uploads/avatars/1.jpg",
        "star_count": 50
    }
}
```

### 3. 注册

#### 接口地址
`POST /api/auth/register`

#### 请求体
```json
{
    "username": "newparent",
    "email": "newparent@example.com",
    "password": "securePassword123",
    "phone": "13800138000"
}
```

#### 响应示例
```json
{
    "message": "Registration successful. Please verify your email.",
    "user_id": 3
}
```

### 4. 刷新Token

#### 接口地址
`POST /api/auth/refresh`

#### 请求体
```json
{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 响应示例
```json
{
    "access_token": "new_access_token...",
    "token_type": "bearer"
}
```

### 5. 登出

#### 接口地址
`POST /api/auth/logout`

#### 请求头
```
Authorization: Bearer {access_token}
```

#### 响应示例
```json
{
    "message": "Logged out successfully"
}
```

## 小朋友管理接口

### 1. 获取小朋友列表

#### 接口地址
`GET /api/children`

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| skip | integer | 否 | 跳过记录数，默认0 |
| limit | integer | 否 | 返回记录数，默认100 |

#### 响应示例
```json
[
    {
        "id": 1,
        "name": "小明",
        "birthday": "2018-05-20",
        "gender": "boy",
        "avatar": "/uploads/avatars/1.jpg",
        "star_count": 50,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-02T00:00:00Z"
    },
    {
        "id": 2,
        "name": "小红",
        "birthday": "2019-03-15",
        "gender": "girl",
        "avatar": "/uploads/avatars/2.jpg",
        "star_count": 35,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-02T00:00:00Z"
    }
]
```

### 2. 获取小朋友详情

#### 接口地址
`GET /api/children/{child_id}`

#### 路径参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| child_id | integer | 是 | 小朋友ID |

#### 响应示例
```json
{
    "id": 1,
    "name": "小明",
    "birthday": "2018-05-20",
    "gender": "boy",
    "avatar": "/uploads/avatars/1.jpg",
    "star_count": 50,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-02T00:00:00Z",
    "recent_records": [
        {
            "id": 10,
            "amount": 5,
            "type": "add",
            "reason": "帮助做家务",
            "created_at": "2024-01-02T10:00:00Z"
        },
        {
            "id": 9,
            "amount": -10,
            "type": "redeem",
            "reason": "兑换玩具",
            "reward_id": 1,
            "created_at": "2024-01-01T15:00:00Z"
        }
    ]
}
```

### 3. 创建小朋友

#### 接口地址
`POST /api/children`

#### 请求体
```json
{
    "name": "小明",
    "birthday": "2018-05-20",
    "gender": "boy",
    "avatar": "base64_encoded_image_data"  // 可选
}
```

#### 请求参数说明
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| name | string | 是 | 姓名，1-100字符 |
| birthday | string | 否 | 生日，格式：YYYY-MM-DD |
| gender | string | 是 | 性别，可选值：boy/girl |
| avatar | string | 否 | 头像图片的base64编码 |

#### 响应示例
```json
{
    "id": 3,
    "name": "小明",
    "birthday": "2018-05-20",
    "gender": "boy",
    "avatar": "/uploads/avatars/3.jpg",
    "star_count": 0,
    "created_at": "2024-01-03T00:00:00Z",
    "updated_at": "2024-01-03T00:00:00Z"
}
```

### 4. 更新小朋友信息

#### 接口地址
`PATCH /api/children/{child_id}`

#### 路径参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| child_id | integer | 是 | 小朋友ID |

#### 请求体
```json
{
    "name": "小明明",
    "birthday": "2018-05-21",
    "avatar": "new_base64_encoded_image_data"
}
```

#### 请求参数说明
所有字段均为可选，只更新提供的字段

#### 响应示例
```json
{
    "id": 1,
    "name": "小明明",
    "birthday": "2018-05-21",
    "gender": "boy",
    "avatar": "/uploads/avatars/1_new.jpg",
    "star_count": 50,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-03T10:00:00Z"
}
```

### 5. 删除小朋友

#### 接口地址
`DELETE /api/children/{child_id}`

#### 路径参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| child_id | integer | 是 | 小朋友ID |

#### 响应示例
```json
{
    "message": "Child deleted successfully"
}
```

## 星星操作接口

### 1. 增加星星

#### 接口地址
`POST /api/children/{child_id}/stars/add`

#### 路径参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| child_id | integer | 是 | 小朋友ID |

#### 请求体
```json
{
    "amount": 10,
    "reason": "完成作业"
}
```

#### 请求参数说明
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| amount | integer | 是 | 增加的星星数量，必须大于0 |
| reason | string | 否 | 增加原因，最多255字符 |

#### 响应示例
```json
{
    "message": "Stars added successfully",
    "new_total": 60,
    "record": {
        "id": 11,
        "child_id": 1,
        "amount": 10,
        "type": "add",
        "reason": "完成作业",
        "created_at": "2024-01-03T11:00:00Z"
    }
}
```

### 2. 减少星星

#### 接口地址
`POST /api/children/{child_id}/stars/subtract`

#### 路径参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| child_id | integer | 是 | 小朋友ID |

#### 请求体
```json
{
    "amount": 5,
    "reason": "违反规则"
}
```

#### 请求参数说明
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| amount | integer | 是 | 减少的星星数量，必须大于0 |
| reason | string | 否 | 减少原因，最多255字符 |

#### 响应示例
```json
{
    "message": "Stars subtracted successfully",
    "new_total": 55,
    "record": {
        "id": 12,
        "child_id": 1,
        "amount": -5,
        "type": "subtract",
        "reason": "违反规则",
        "created_at": "2024-01-03T12:00:00Z"
    }
}
```

#### 错误响应
当星星不足时：
```json
{
    "error": "Insufficient stars",
    "status_code": 400,
    "current_stars": 5,
    "requested": 10
}
```

### 3. 获取星星记录

#### 接口地址
`GET /api/children/{child_id}/stars/records`

#### 路径参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| child_id | integer | 是 | 小朋友ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| skip | integer | 否 | 跳过记录数，默认0 |
| limit | integer | 否 | 返回记录数，默认20 |
| type | string | 否 | 筛选类型：add/subtract/redeem |

#### 响应示例
```json
[
    {
        "id": 12,
        "child_id": 1,
        "amount": -5,
        "type": "subtract",
        "reason": "违反规则",
        "created_at": "2024-01-03T12:00:00Z"
    },
    {
        "id": 11,
        "child_id": 1,
        "amount": 10,
        "type": "add",
        "reason": "完成作业",
        "created_at": "2024-01-03T11:00:00Z"
    }
]
```

## 奖品管理接口

### 1. 获取奖品列表

#### 接口地址
`GET /api/rewards`

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| child_id | integer | 否 | 按小朋友ID筛选 |
| is_redeemed | boolean | 否 | 筛选兑换状态 |
| skip | integer | 否 | 跳过记录数，默认0 |
| limit | integer | 否 | 返回记录数，默认100 |

#### 响应示例
```json
[
    {
        "id": 1,
        "name": "乐高积木",
        "image": "/uploads/rewards/1.jpg",
        "required_stars": 100,
        "description": "大型乐高城堡套装",
        "is_redeemed": false,
        "created_at": "2024-01-01T00:00:00Z",
        "children": [
            {
                "id": 1,
                "name": "小明",
                "current_stars": 55,
                "progress": 55
            },
            {
                "id": 2,
                "name": "小红",
                "current_stars": 35,
                "progress": 35
            }
        ]
    }
]
```

### 2. 获取奖品详情

#### 接口地址
`GET /api/rewards/{reward_id}`

#### 路径参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| reward_id | integer | 是 | 奖品ID |

#### 响应示例
```json
{
    "id": 1,
    "name": "乐高积木",
    "image": "/uploads/rewards/1.jpg",
    "required_stars": 100,
    "description": "大型乐高城堡套装",
    "is_redeemed": false,
    "redeemed_at": null,
    "created_at": "2024-01-01T00:00:00Z",
    "children": [
        {
            "id": 1,
            "name": "小明",
            "avatar": "/uploads/avatars/1.jpg",
            "current_stars": 55,
            "progress": 55,
            "deduction_amount": null
        },
        {
            "id": 2,
            "name": "小红",
            "avatar": "/uploads/avatars/2.jpg",
            "current_stars": 35,
            "progress": 35,
            "deduction_amount": null
        }
    ]
}
```

### 3. 创建奖品

#### 接口地址
`POST /api/rewards`

#### 请求体
```json
{
    "name": "遥控汽车",
    "required_stars": 50,
    "description": "高速遥控赛车",
    "image": "base64_encoded_image_data",
    "child_ids": [1, 2]
}
```

#### 请求参数说明
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| name | string | 是 | 奖品名称，1-100字符 |
| required_stars | integer | 是 | 所需星星数，必须大于0 |
| description | string | 否 | 奖品描述 |
| image | string | 否 | 奖品图片的base64编码 |
| child_ids | array | 是 | 关联的小朋友ID数组 |

#### 响应示例
```json
{
    "id": 2,
    "name": "遥控汽车",
    "image": "/uploads/rewards/2.jpg",
    "required_stars": 50,
    "description": "高速遥控赛车",
    "is_redeemed": false,
    "created_at": "2024-01-03T13:00:00Z",
    "children": [
        {
            "id": 1,
            "name": "小明"
        },
        {
            "id": 2,
            "name": "小红"
        }
    ]
}
```

### 4. 更新奖品信息

#### 接口地址
`PATCH /api/rewards/{reward_id}`

#### 路径参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| reward_id | integer | 是 | 奖品ID |

#### 请求体
```json
{
    "name": "超级遥控汽车",
    "required_stars": 60,
    "child_ids": [1, 2, 3]
}
```

#### 请求参数说明
所有字段均为可选，只更新提供的字段

#### 响应示例
```json
{
    "id": 2,
    "name": "超级遥控汽车",
    "image": "/uploads/rewards/2.jpg",
    "required_stars": 60,
    "description": "高速遥控赛车",
    "is_redeemed": false,
    "created_at": "2024-01-03T13:00:00Z",
    "updated_at": "2024-01-03T14:00:00Z"
}
```

### 5. 删除奖品

#### 接口地址
`DELETE /api/rewards/{reward_id}`

#### 路径参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| reward_id | integer | 是 | 奖品ID |

#### 响应示例
```json
{
    "message": "Reward deleted successfully"
}
```

### 6. 兑换奖品

#### 接口地址
`POST /api/rewards/{reward_id}/redeem`

#### 路径参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| reward_id | integer | 是 | 奖品ID |

#### 请求体
```json
{
    "deductions": [
        {
            "child_id": 1,
            "amount": 60
        },
        {
            "child_id": 2,
            "amount": 40
        }
    ]
}
```

#### 请求参数说明
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| deductions | array | 是 | 扣除明细数组 |
| deductions[].child_id | integer | 是 | 小朋友ID |
| deductions[].amount | integer | 是 | 扣除星星数，必须大于0 |

#### 响应示例
```json
{
    "message": "Reward redeemed successfully",
    "total_stars_deducted": 100,
    "reward": {
        "id": 1,
        "name": "乐高积木",
        "is_redeemed": true,
        "redeemed_at": "2024-01-03T15:00:00Z"
    },
    "records": [
        {
            "child_id": 1,
            "child_name": "小明",
            "deducted": 60,
            "remaining_stars": 0
        },
        {
            "child_id": 2,
            "child_name": "小红",
            "deducted": 40,
            "remaining_stars": 0
        }
    ]
}
```

#### 错误响应

##### 奖品已兑换
```json
{
    "error": "Reward already redeemed",
    "status_code": 400
}
```

##### 星星不足
```json
{
    "error": "小明 has insufficient stars",
    "status_code": 400,
    "child_id": 1,
    "current_stars": 30,
    "requested": 60
}
```

## 文件上传接口

### 1. 上传头像

#### 接口地址
`POST /api/upload/avatar`

#### 请求格式
`multipart/form-data`

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| file | file | 是 | 图片文件，支持jpg/png/gif，最大5MB |

#### 响应示例
```json
{
    "url": "/uploads/avatars/20240103_150000_abc123.jpg",
    "thumbnail": "/uploads/avatars/thumb_20240103_150000_abc123.jpg",
    "size": 102400,
    "type": "image/jpeg"
}
```

### 2. 上传奖品图片

#### 接口地址
`POST /api/upload/reward`

#### 请求格式
`multipart/form-data`

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| file | file | 是 | 图片文件，支持jpg/png/gif，最大10MB |

#### 响应示例
```json
{
    "url": "/uploads/rewards/20240103_151000_xyz789.jpg",
    "thumbnail": "/uploads/rewards/thumb_20240103_151000_xyz789.jpg",
    "size": 204800,
    "type": "image/jpeg"
}
```

## 项目管理接口

### 1. 获取项目列表

#### 接口地址
`GET /api/projects`

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| type | string | 否 | 项目类型：add/subtract |
| category | string | 否 | 项目分类 |
| is_active | boolean | 否 | 是否启用 |

#### 响应示例
```json
[
    {
        "id": 1,
        "name": "完成作业",
        "type": "add",
        "value": 5,
        "category": "学习",
        "icon": "📚",
        "repeat_rule": "daily",
        "is_active": true,
        "applicable_children": [1, 2],
        "usage_count": 45
    },
    {
        "id": 2,
        "name": "不按时睡觉",
        "type": "subtract",
        "value": 2,
        "category": "生活",
        "icon": "🛌",
        "repeat_rule": "unlimited",
        "is_active": true,
        "applicable_children": [1],
        "usage_count": 12
    }
]
```

### 2. 创建项目

#### 接口地址
`POST /api/projects`

#### 请求体
```json
{
    "name": "阅读30分钟",
    "type": "add",
    "value": 3,
    "category": "学习",
    "description": "每天坚持阅读30分钟",
    "icon": "📖",
    "repeat_rule": "daily",
    "applicable_children": [1, 2]
}
```

#### 响应示例
```json
{
    "id": 3,
    "name": "阅读30分钟",
    "type": "add",
    "value": 3,
    "category": "学习",
    "description": "每天坚持阅读30分钟",
    "icon": "📖",
    "repeat_rule": "daily",
    "is_active": true,
    "created_at": "2024-01-03T10:00:00Z"
}
```

### 3. 更新项目

#### 接口地址
`PUT /api/projects/{project_id}`

#### 请求体
```json
{
    "value": 4,
    "is_active": true,
    "applicable_children": [1, 2, 3]
}
```

#### 响应示例
```json
{
    "message": "Project updated successfully",
    "project": {
        "id": 3,
        "name": "阅读30分钟",
        "value": 4,
        "is_active": true
    }
}
```

### 4. 删除项目

#### 接口地址
`DELETE /api/projects/{project_id}`

#### 响应示例
```json
{
    "message": "Project deleted successfully"
}
```

### 5. 使用项目快速加减星

#### 接口地址
`POST /api/projects/{project_id}/apply`

#### 请求体
```json
{
    "child_ids": [1, 2],
    "note": "今天表现很好"
}
```

#### 响应示例
```json
{
    "message": "Stars updated successfully",
    "results": [
        {
            "child_id": 1,
            "child_name": "小明",
            "stars_changed": 5,
            "new_total": 55
        },
        {
            "child_id": 2,
            "child_name": "小红",
            "stars_changed": 5,
            "new_total": 40
        }
    ]
}
```

## 数据分析接口

### 1. 获取每日总结

#### 接口地址
`GET /api/analytics/daily-summary`

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| date | string | 否 | 日期，格式：YYYY-MM-DD，默认今天 |

#### 响应示例
```json
{
    "date": "2024-01-03",
    "overall": {
        "total_stars_earned": 85,
        "total_stars_spent": 30,
        "active_children": 4,
        "best_performer": {
            "id": 1,
            "name": "小明",
            "stars_earned": 35
        }
    },
    "children_summaries": [
        {
            "child_id": 1,
            "child_name": "小明",
            "star_changes": {
                "earned": 35,
                "spent": 10,
                "net": 25
            },
            "completed_projects": [
                {"name": "完成作业", "count": 2},
                {"name": "帮助家务", "count": 1}
            ],
            "behavior_score": 85,
            "mood": "happy"
        }
    ],
    "insights": {
        "trend": "improving",
        "key_observations": [
            "小明今天的表现明显进步",
            "整体完成任务数量比昨天增加30%"
        ],
        "recommendations": [
            "建议增加运动类项目",
            "小红需要更多鼓励"
        ]
    }
}
```

### 2. 获取趋势数据

#### 接口地址
`GET /api/analytics/trends`

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| child_id | integer | 否 | 小朋友ID，不传则返回所有 |
| period | string | 否 | 时间段：week/month/year |
| start_date | string | 否 | 开始日期 |
| end_date | string | 否 | 结束日期 |

#### 响应示例
```json
{
    "period": "week",
    "data": [
        {
            "date": "2024-01-01",
            "children": [
                {"id": 1, "name": "小明", "stars": 120},
                {"id": 2, "name": "小红", "stars": 100}
            ]
        },
        {
            "date": "2024-01-02",
            "children": [
                {"id": 1, "name": "小明", "stars": 125},
                {"id": 2, "name": "小红", "stars": 105}
            ]
        }
    ],
    "summary": {
        "total_change": 15,
        "average_daily": 7.5,
        "trend": "upward"
    }
}
```

### 3. 获取行为分析

#### 接口地址
`GET /api/analytics/behavior`

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| child_id | integer | 是 | 小朋友ID |
| period | string | 否 | 分析周期：week/month |

#### 响应示例
```json
{
    "child_id": 1,
    "child_name": "小明",
    "period": "week",
    "behavior_distribution": {
        "学习": 45,
        "生活": 30,
        "运动": 15,
        "社交": 10
    },
    "peak_activity_time": {
        "hour": 19,
        "description": "晚上7点最活跃"
    },
    "consistent_behaviors": [
        "每天完成作业",
        "按时睡觉"
    ],
    "improvement_areas": [
        "运动量不足",
        "社交互动较少"
    ],
    "recommendations": [
        "增加户外活动时间",
        "安排更多小朋友互动"
    ]
}
```

### 4. 生成报表

#### 接口地址
`POST /api/analytics/reports`

#### 请求体
```json
{
    "type": "weekly",
    "start_date": "2024-01-01",
    "child_ids": [1, 2],
    "format": "pdf",
    "email_to": "parent@example.com"
}
```

#### 响应示例
```json
{
    "report_id": "rpt_20240103_001",
    "status": "generating",
    "estimated_time": 30,
    "download_url": "/api/reports/download/rpt_20240103_001"
}
```

### 5. 下载报表

#### 接口地址
`GET /api/reports/download/{report_id}`

#### 响应
返回PDF或Excel文件流

## 管理后台接口

### 1. 获取仪表盘数据

#### 接口地址
`GET /api/admin/dashboard`

#### 响应示例
```json
{
    "stats": {
        "total_stars": 1250,
        "weekly_change": 85,
        "pending_rewards": 3,
        "active_children": 4
    },
    "recent_activities": [
        {
            "type": "star_added",
            "child_name": "小明",
            "amount": 5,
            "reason": "完成作业",
            "time": "2024-01-03T15:30:00Z"
        }
    ],
    "pending_requests": [
        {
            "id": 1,
            "type": "reward_redemption",
            "child_name": "小红",
            "reward_name": "乐高积木",
            "requested_at": "2024-01-03T14:00:00Z"
        }
    ],
    "quick_stats": {
        "today_stars_earned": 45,
        "today_tasks_completed": 12,
        "week_best_performer": "小明"
    }
}
```

### 2. 批量操作小朋友

#### 接口地址
`POST /api/admin/children/batch`

#### 请求体
```json
{
    "action": "add_stars",
    "child_ids": [1, 2, 3],
    "data": {
        "amount": 10,
        "reason": "周末集体活动表现优秀"
    }
}
```

#### 响应示例
```json
{
    "success": true,
    "results": [
        {"child_id": 1, "status": "success", "new_total": 60},
        {"child_id": 2, "status": "success", "new_total": 45},
        {"child_id": 3, "status": "success", "new_total": 55}
    ]
}
```

### 3. 系统设置

#### 接口地址
`GET /api/admin/settings`

#### 响应示例
```json
{
    "general": {
        "site_name": "我的星星存折",
        "theme": "default",
        "language": "zh-CN"
    },
    "rules": {
        "daily_star_limit": 50,
        "min_stars_balance": 0,
        "allow_negative": false
    },
    "notifications": {
        "email_enabled": true,
        "daily_summary_time": "20:00",
        "weekly_report_day": "sunday"
    }
}
```

### 4. 更新系统设置

#### 接口地址
`PUT /api/admin/settings`

#### 请求体
```json
{
    "rules": {
        "daily_star_limit": 100,
        "allow_negative": true
    }
}
```

#### 响应示例
```json
{
    "message": "Settings updated successfully",
    "updated_fields": ["rules.daily_star_limit", "rules.allow_negative"]
}
```

## 统计接口

### 1. 获取统计概览

#### 接口地址
`GET /api/stats/overview`

#### 响应示例
```json
{
    "total_children": 5,
    "total_stars": 250,
    "total_rewards": 10,
    "redeemed_rewards": 3,
    "pending_rewards": 7,
    "recent_activities": [
        {
            "type": "star_added",
            "child_name": "小明",
            "amount": 10,
            "time": "2024-01-03T10:00:00Z"
        },
        {
            "type": "reward_redeemed",
            "reward_name": "乐高积木",
            "children": ["小明", "小红"],
            "time": "2024-01-03T09:00:00Z"
        }
    ]
}
```

### 2. 获取小朋友统计

#### 接口地址
`GET /api/children/{child_id}/stats`

#### 路径参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| child_id | integer | 是 | 小朋友ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| start_date | string | 否 | 开始日期，格式：YYYY-MM-DD |
| end_date | string | 否 | 结束日期，格式：YYYY-MM-DD |

#### 响应示例
```json
{
    "child_id": 1,
    "child_name": "小明",
    "current_stars": 55,
    "total_earned": 150,
    "total_spent": 95,
    "rewards_redeemed": 2,
    "monthly_stats": [
        {
            "month": "2024-01",
            "earned": 50,
            "spent": 30
        },
        {
            "month": "2023-12",
            "earned": 100,
            "spent": 65
        }
    ],
    "top_earning_reasons": [
        {
            "reason": "完成作业",
            "count": 15,
            "total_stars": 75
        },
        {
            "reason": "帮助家务",
            "count": 10,
            "total_stars": 50
        }
    ]
}
```

## WebSocket接口（规划中）

### 实时通知

#### 连接地址
`ws://localhost:8000/ws/{client_id}`

#### 消息格式
```json
{
    "type": "star_update",
    "data": {
        "child_id": 1,
        "new_total": 65,
        "change": 10,
        "reason": "完成作业"
    }
}
```

#### 消息类型
- `star_update`: 星星变动通知
- `reward_created`: 新奖品创建
- `reward_redeemed`: 奖品兑换通知
- `child_updated`: 小朋友信息更新

## 错误码对照表

| 错误码 | 说明 | 处理建议 |
|--------|------|---------|
| 1001 | 小朋友不存在 | 检查ID是否正确 |
| 1002 | 星星余额不足 | 减少扣除数量或增加星星 |
| 1003 | 奖品已兑换 | 选择其他奖品 |
| 1004 | 文件类型不支持 | 使用jpg/png/gif格式 |
| 1005 | 文件大小超限 | 压缩文件或选择更小的文件 |
| 1006 | 数据验证失败 | 检查请求参数格式 |
| 1007 | 重复的小朋友姓名 | 使用不同的姓名 |
| 1008 | 奖品不存在 | 检查奖品ID |
| 1009 | 关联关系不存在 | 检查小朋友与奖品的关联 |
| 1010 | 操作权限不足 | 登录或获取权限 |

## 版本历史

### v1.0.0 (2024-01-01)
- 初始版本发布
- 基础的增删改查功能
- 星星管理系统
- 奖品兑换功能

### v1.1.0 (规划中)
- 添加用户认证系统
- WebSocket实时通知
- 数据导出功能
- 批量操作接口

### v1.2.0 (规划中)
- 任务系统
- 成就徽章
- 数据分析仪表板
- 移动端API优化
