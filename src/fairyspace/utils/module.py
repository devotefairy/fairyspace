from importlib import import_module
from importlib.util import find_spec

from fairyspace.const.inner import (
    FAIRY_INNER_CONFIG_FORM,
    FAIRY_INNER_CONFIG_MODULE_DIR,
    FAIRY_INNER_CONFIG_STATEMENT,
    FAIRY_INNER_CONFIG_VIEW,
)


def fairy_load_app_config(app_label, module_slug=None):
    """加载指定应用下的模块"""
    if not module_slug:
        return
    try:
        module_name = f'{app_label}.{FAIRY_INNER_CONFIG_MODULE_DIR}.{module_slug}'
        module = find_spec(module_name)
        if module:
            return import_module(module_name)
    except ModuleNotFoundError:
        return


def fairy_load_global_config(app_label, module_slug=None):
    """加载全局配置模块下的指定应用的模块"""
    try:
        module_name = f'{FAIRY_INNER_CONFIG_MODULE_DIR}.{app_label}.{module_slug}'
        module = find_spec(module_name)
        if module:
            return import_module(module_name)
    except ModuleNotFoundError:
        return


def fairy_load_module(app_label, module_slug):
    """加载全局空间对应的模块和应用空间对应的模块"""
    global_module = fairy_load_global_config(app_label, module_slug)
    app_module = fairy_load_app_config(app_label, module_slug)
    return global_module, app_module


def fairy_load_view(app_label):
    """加载视图"""
    return fairy_load_module(app_label, FAIRY_INNER_CONFIG_VIEW)


def fairy_load_statement(app_label):
    """加载配置声明模块"""
    return fairy_load_module(app_label, FAIRY_INNER_CONFIG_STATEMENT)


def fairy_load_form(app_label):
    """加载认证表单模块"""
    return fairy_load_module(app_label, FAIRY_INNER_CONFIG_FORM)


def import_class_from_string(dotted_path):
    """
    尝试从一个字符串中加载一个类
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ImportError(f"{dotted_path} 不是一个模块路径")

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError(f'模块 {module_path} 没有定义一个 {class_name} 属性/类')
