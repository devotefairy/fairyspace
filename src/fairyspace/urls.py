"""
FairySpace URL Configuration
"""

import copy

from django.conf import settings
from django.urls import path, include

from fairyspace.const import FAIRY_INNER_CONFIG_VIEW
from fairyspace.rest.router import FairySimpleRouter
from fairyspace.rest.views import FairyModelViewSet
from fairyspace.utils.module import import_class_from_string


def make_urls_class(endpoint, attrs):
    """
    根据配置中的端点来生成对应的 URL

    根据指定的 endpoint 和端点对应的配置，动态构建视图，然后自动注册

    Params:
        name    str         端标识符，例如 client, manage, open
        attrs   dict | None 端对应的配置，🚀 包含视图类，视图类对应的配置，各种声明应该是字符串
    """

    # 复制一份 attrs 的副本，避免修改原始的端配置 attrs
    endpoint_attrs = copy.deepcopy(attrs) if attrs and isinstance(attrs, dict) else {}

    # 默认视图的端点是有 endpoint 来指定，这里是为了方便视图类中使用，来根据端的标识
    # 来获取对应端的各种视图，表单等
    endpoint_attrs['fairy_endpoint'] = endpoint

    # 视图类
    view_class = None

    # 检测是否在配置中定义了对应的自定义的视图类
    if endpoint_attrs.get(FAIRY_INNER_CONFIG_VIEW):
        try:
            view_class = import_class_from_string(endpoint_attrs[FAIRY_INNER_CONFIG_VIEW])
        except Exception:
            # 如果配置中找不到对应的视图类，则不进行任何处理，使用默认的视图类
            pass

    # 如果配置中找不到对应的视图类，则使用默认的视图类
    if not view_class:
        view_class = FairyModelViewSet

    view_class_name = f'Fairy{endpoint.title()}ModelViewSet'

    # TODO: 这里需要优化，因为 endpoint_attrs 中可能包含一些不合法的属性，需要进行过滤
    fairy_view_class = type(view_class_name, (view_class,), endpoint_attrs)

    router = FairySimpleRouter(fairy_base_name=f'fairy-{endpoint.lower()}')
    router.register('', fairy_view_class)
    return router.urls


def fairy_get_urls():
    """
    根据配置中的端点来生成对应的 URL
    """
    urlpatterns = []
    endpoints = settings.FAIRY_SPACE_CONFIG.get('endpoints', {})

    if not endpoints or not isinstance(endpoints, dict):
        raise Exception('路由 endpoints 配置应该是一个字典')

    for key, value in endpoints.items():
        urlpatterns.append(
            path(
                f'fairy/{key}/<str:app>/<str:model>/',
                include(make_urls_class(key, value)),
            )
        )
    return urlpatterns


urlpatterns = fairy_get_urls()
