"""
此库内部使用的常量列表

常量格式为 FAIRY_INNER_{名称}
"""

# 检索
FAIRY_INNER_ACTION_RETRIEVE = 'retrieve'
# 增强型的检索
FAIRY_INNER_ACTION_RETRIEVE_ENHANCE = 'retrieve_enhance'
# 检索我的动作
FAIRY_INNER_ACTION_RETRIEVE_MINE = 'retrieve_mine'

# 删除动作
FAIRY_INNER_ACTION_DESTROY = 'destroy'

# 列表
FAIRY_INNER_ACTION_LIST = 'list'
# 增强型的列表
FAIRY_INNER_ACTION_LIST_ENHANCE = 'list_enhance'
# 检索我的列表动作
FAIRY_INNER_ACTION_LIST_MINE = 'list_mine'

# 创建动作
FAIRY_INNER_ACTION_CREATE = 'create'

# 更新动作
FAIRY_INNER_ACTION_UPDATE = 'update'
# 部分更新
FAIRY_INNER_ACTION_PARTIAL_UPDATE = 'partial_update'
# PUT 型的部分更新
FAIRY_INNER_ACTION_PATCH_ENHANCE = 'patch_enhance'

# 云函数动作
FAIRY_INNER_ACTION_CLOUD_FUNC = 'cloudfunc'

# 批量处理的动作
FAIRY_INNER_ACTION_BATCH_HANDLE = 'batch'

# 导出文件的动作
FAIRY_INNER_ACTION_EXPORT_FILE = 'export'

# 配置文件夹和配置文件名称

# 放全局的文件夹名称
FAIRY_INNER_CONFIG_MODULE_DIR = 'fairyconfig'

# 处理的视图
FAIRY_INNER_CONFIG_VIEW = 'view'

# 声明配置类
FAIRY_INNER_CONFIG_STATEMENT = 'statement'

# 自定义校验表单
FAIRY_INNER_CONFIG_FORM = 'form'

# 管理后台自定义的导出序列化类
FAIRY_INNER_CONFIG_EXPORT = 'export'
