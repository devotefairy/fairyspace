# 单元测试通用规则

**核心原则：简洁优先**

## 组织与命名

-   类 Test{Feature}；方法 test*{功能}*{场景}
-   辅助函数动词开头 make*{对象}、assert*{条件}
-   确保符合 AAA 模式 Arrange-Act-Assert

## 约定

-   为测试类和方法添加 Docstring 描述功能场景
-   使用 pytest；断言直接使用 assert 并提供清晰失败信息
-   复杂初始化使用 @pytest.fixture 封装
-   使用异常测试 with pytest.raises(ExpectedError) 捕获预期错误
-   使用参数化测试 @pytest.mark.parametrize，使用 ids 参数增强可读性
-   Mock 仅用于外部依赖，避免模拟业务逻辑
-   当方法超过 30 行或嵌套 > 5 层时应拆分或提取辅助方法

## 覆盖率目标

-   核心业务行覆盖率 ≥ 90%
-   工具/辅助模块 ≥ 70%
