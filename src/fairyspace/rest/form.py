from rest_framework import serializers
from fairyspace.utils.module import fairy_load_form


def create_meta_class(model):
    """构建 Meta 类"""

    attrs = {'model': model, 'fields': '__all__'}

    return type('Meta', (object,), attrs)


def create_form_class(model, action=''):
    """构建表单序列化类"""

    def __init__(self, *args, **kwargs):
        super(serializers.ModelSerializer, self).__init__(*args, **kwargs)

    attrs = {'Meta': create_meta_class(model), '__init__': __init__}

    class_name = f'Fairy{model.__name__}{action}Form'

    return type(class_name, (serializers.ModelSerializer,), attrs)


def fairy_get_form_class(view, action):
    """获取表单类

    FIXME: 这里为什么还要填 action 参数，而不是通过 self.action 进行获取，因为在其他地方，需要创建对应的表单时，
    可以灵活指定对应的 action，例如云函数中，创建对应的表单，self.action 是 cloudfunc，但是此时想创建一个 create
    对应的表单时，可以调用传入的 action 是 create 而不是 cloudfunc

    Params:
        view    object 视图对象
        action  string 方法名

    Returns:
        class 表单类
    """

    action_map = {
        'create': 'Create',
        'update': 'Update',
        'partial_update': 'PartialUpdate',
        'patch_enhance': 'PatchEnhance',
    }

    def get_form_class(form_module):
        if not form_module:
            return

        action_name = action_map.get(action)
        model_title = view.fairy_instance.model.__name__
        class_name = f'{model_title}{action_name}{view.fairy_endpoint.title()}Form'
        return getattr(form_module, class_name, None)

    global_form_module, app_form_module = fairy_load_form(view.fairy_instance.app_label)

    form_list = [get_form_class(global_form_module), get_form_class(app_form_module)]
    form_list = tuple((item for item in form_list if item))

    # 如果存在，则返回第一个
    if form_list:
        return form_list[0]

    # 如果都不存在，则创建一个
    return create_form_class(view.fairy_instance.model, action)


class FairyFormMixin:
    """数据验证表单"""

    def get_validate_form(self, action):
        """获取数据校验表单"""
        return fairy_get_form_class(self, action)
