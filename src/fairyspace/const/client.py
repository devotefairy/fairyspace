"""
客户端使用的常量列表

例如客户端和管理端，或者其他端传递数据的标准

常量命名格式为 FAIRY_CLIENT_{名称}
"""

"""
请求端传入 fairyspace 的命名空间

即过滤条件，展示字段等等，即跟业务数据无关的都会放到此命名空间下

例如，客户端传进来的数据格式为：

{
    'fairyspace': {
        'fields': ['id', 'name'],
        'filters': [
            {field: id, operator: '=', value: 2},
            ...
        ]
        ...
    },
    data: 具体的业务数据
}
"""
FAIRY_CLIENT_NAMESPACE = 'fairyspace'

"""
接口请求返回展示的字段

数据格式 <列表>

示例
    ['id', 'name', {'user': ['nick_name']}]
"""
FAIRY_CLIENT_DISPLAY_FIELD_LIST = 'fields'

"""
客户端传入过滤条件的命名空间

通过此进行数据过滤和筛选

支持的方法：如果在 body 中传入过滤条件都支持
数据格式 <List>

示例：

    [
        {
            'field': 字段名，
            'operator': 运算符，
            'value': 值，
            'type': object_property 默认为空
        },
        ...
    ]
"""
FAIRY_CLIENT_QUERY_FILTER_LIST = 'filters'

"""
函数声明：云函数或者批量函数的名称

例如：

    {
        'func': 'func_name'
    }
"""
FAIRY_CLIENT_CLOUD_FUNC_NAME = 'func'

"""
访问端传入使用导出配置中的哪个索引 Key
"""
FAIRY_CLIENT_EXPORT_DATA_KEY = 'export'
