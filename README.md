# fairyspace

基于 Django REST framework 的模型即接口框架

**"零代码/低代码"的 Django REST API 框架**，通过约定和配置的方式，让开发者能够快速构建功能完整、性能优良的 REST API，大大减少了重复的样板代码编写。

[![PyPI - Version](https://img.shields.io/pypi/v/fairyapi.svg)](https://pypi.org/project/fairyspace)
[![Python Version](https://img.shields.io/badge/python-%3E%3D3.11-green)](https://pypi.org/project/fairyspace)

---

## 安装

```console
pip install fairyspace
```

## 核心功能

### 1 动态 API 生成
- 通过 URL 路由 `fairy/{endpoint}/{app}/{model}/` 自动为任何 Django 模型生成完整的 REST API
- 支持多端点配置（如 client、manage、open 等不同的访问端）
- 无需为每个模型手写 ViewSet 和 Serializer

### 2 统一的数据交互格式
```python
# 请求格式
{
    'fairyspace': {  # 框架命名空间
        'fields': ['id', 'name'],  # 指定返回字段
        'filters': [...],          # 过滤条件
        'func': 'function_name'    # 云函数名称
    },
    'data': {}  # 业务数据
}

# 响应格式
{
    'code': 0,
    'message': '',
    'result': data
}
```

### 3 灵活的字段控制

- **动态字段选择**：客户端可指定需要返回的字段
- **关联数据预取**：自动处理 `prefetch_related` 优化查询
- **嵌套序列化**：支持深层关联数据的序列化
- **计算属性**：通过 `@fairyproperty` 装饰器支持计算字段

### 4 多层级配置系统

支持三个层级的自定义配置：
- **全局配置**：`fairyconfig/` 目录下的全局配置
- **应用配置**：各应用下的 `fairyconfig/` 配置
- **方法级配置**：具体 action 方法的配置

### 5 增强的 CRUD 操作

```python
# 标准 REST 操作
GET    /fairy/client/school/student/     # list
POST   /fairy/client/school/student/     # create
GET    /fairy/client/school/student/1/   # retrieve
PUT    /fairy/client/school/student/1/   # update
DELETE /fairy/client/school/student/1/   # destroy

# 增强操作
POST   /fairy/client/school/student/list/        # 增强列表查询
POST   /fairy/client/school/student/list/mine/   # 获取我的数据
POST   /fairy/client/school/student/1/retrieve/  # 增强详情查询
POST   /fairy/client/school/student/cloudfunc/   # 云函数调用
POST   /fairy/client/school/student/batch/       # 批量操作
```

### 6 云函数和批量处理

- **云函数**：支持自定义业务逻辑函数
- **批量操作**：支持批量处理多条数据
- **事务支持**：自动包装数据库事务

### 7 用户数据自动注入

- 创建/更新时自动注入当前登录用户信息
- 支持用户数据过滤（只看自己的数据）
- 可配置的用户字段处理策略

### 8 权限和认证的灵活配置

- 支持方法级、视图级、全局级的权限配置
- 动态权限类加载
- 支持多种认证方式

## 设计亮点

### 1 约定优于配置
- 通过命名约定自动发现和加载配置类
- 默认行为覆盖大部分使用场景，特殊需求可通过配置覆盖

### 2 高度可扩展
- 插件化的配置系统
- 支持自定义 ViewSet、Form、Statement 等
- 装饰器模式支持功能增强

### 3 性能优化
- 智能的关联查询优化
- 动态序列化类生成
- 字段级别的查询控制

## 适用场景

这个框架特别适合：
- **快速原型开发**：无需手写大量重复的 API 代码
- **管理后台**：需要对多个模型进行 CRUD 操作
- **多端应用**：同一套数据模型需要为不同端（客户端、管理端、开放API）提供不同的接口
- **数据导出**：内置的导出功能
- **权限复杂的系统**：灵活的权限配置系统

