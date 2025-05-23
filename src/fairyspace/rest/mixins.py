from django.db import transaction
from django.apps import apps

from rest_framework.decorators import action
from rest_framework import serializers

from fairyspace import const
from fairyspace.core import exception
from fairyspace.rest.response import success_response
from fairyspace.rest.user_pip import fairy_pip_user_add_handle
from fairyspace.utils import meta, data
from fairyspace.utils.module import fairy_load_statement, fairy_load_view


class FairyMixin:
    """添加的自定义业务处理"""

    def fairy_rewrite_permission_class(self):
        """重置"""
        pass

    def fairy_get_statements(self):
        """获取配置声明类"""

        def get_statements(statement_module):
            if not statement_module:
                return

            model_title = self.fairy_instance.model.__name__
            class_name = f'{model_title}{self.fairy_endpoint.title()}Statements'
            return getattr(statement_module, class_name, None)

        statement_class = None
        global_statements, app_statements = fairy_load_statement(self.fairy_instance.app_label)

        class_list = [get_statements(global_statements), get_statements(app_statements)]
        class_list = tuple((item for item in class_list if item))
        if class_list:
            statement_class = type('FairyStatementConfig', class_list, {})
        self.fairy_instance.statement_class = statement_class

    def fairy_get_custom_view_instance(self):
        """
        获取用户自定义的顶级命名空间的视图对象和应用空间下的视图对象

        即自定义在 views.py 中，

        格式为 '{model_title}{self.fairy_endpoint.title()}ViewSet'

        的对象
        """

        def get_view_class(view_module):
            if not view_module:
                return

            model_title = self.fairy_instance.model.__name__
            view_class_name = f'{model_title}{self.fairy_endpoint.title()}ViewSet'
            return getattr(view_module, view_class_name, None)

        # 先查询对应的全局视图
        top_module, app_module = fairy_load_view(self.fairy_instance.app_label)
        class_list = [get_view_class(top_module), get_view_class(app_module)]
        class_list = tuple((item for item in class_list if item))

        if class_list:
            custom_views = type('FairyCustomViewSet', class_list, {})
            self.fairy_instance.custom_view_instance = custom_views()

    def fairy_custom_action_handler(self):
        """
        从模块中找对应的处理器，这里的处理器都是对应每个 action，用户
        可以在全局空间和应用空间下重写对应的 action（例如 list，retrieve 等等)

        获取到对应请求接收处理器后，后续针对权限，认证，限流等等类的处理，划分为三个级别

        - 具体方法级别的配置类（权限，认证等等）
        - 具体应用自定义视图指定的配置类
        - 最顶级基础入口级别的配置类
        """
        custom_view_instance = self.fairy_instance.custom_view_instance

        if custom_view_instance:
            action_name = self.action

            if self.action == 'cloudfunc':
                func_name = self.fairy_instance.request_namespace.get(const.FAIRY_CLIENT_CLOUD_FUNC_NAME)
                action_name = f'cloudfunc_{func_name}'
            elif self.action == 'batch':
                func_name = self.fairy_instance.request_namespace.get(const.FAIRY_CLIENT_CLOUD_FUNC_NAME)
                action_name = f'batch_{func_name}'

            self.fairy_instance.custom_action_handler = getattr(custom_view_instance, action_name, None)

    def fairy_get_request_namespace(self, request, *args, **kwargs):
        """获取请求端命名空间对应的参数

        请求端传入的格式：
        {
            fairyspace: {
                expand_fields: [],
                display_fields: [],
                ....
            },
            data: 数据
        }
        """
        self.fairy_instance.request_namespace = request.data.get(const.FAIRY_CLIENT_NAMESPACE, {})
        if not isinstance(self.fairy_instance.request_namespace, dict):
            self.fairy_instance.request_namespace = {}

    def fairy_get_model(self, request, *args, **kwargs):
        """
        获取模型
        """
        self.fairy_instance.app_label = self.kwargs.get('app')
        self.fairy_instance.model_label = self.kwargs.get('model')
        self.fairy_instance.model = apps.get_model(self.fairy_instance.app_label, self.fairy_instance.model_label)

    def fairy_get_expand_fields(self, request, *args, **kwargs):
        """获取扩展字段

        这里通过客户端传递过来的 display_fields 进行扩展字段的筛选和处理
        """
        try:
            self.fairy_instance.display_fields = self.fairy_instance.request_namespace.get(
                const.FAIRY_CLIENT_DISPLAY_FIELD_LIST
            )
            self.fairy_instance.expand_fields = data.get_prefetch_fields(self.fairy_instance.display_fields)

            self.fairy_translate_expand_fields(self.fairy_instance.expand_fields)
        except Exception:
            pass

    def fairy_translate_expand_fields(self, expand_fields):
        """转换展开字段

        例如

        article.tag.user 会转换成 article.tag_set.user

        即 article.tag.user 中包含虚拟关系字段，则会转换为虚拟关系字段的 accessor name

        这里做转换，是为了后续做 prefetch_related
        """
        if not self.fairy_instance.expand_fields:
            return

        if self.fairy_instance.transform_expand_fields:
            return

        result = []
        for _, item in enumerate(expand_fields):
            field_list, model = item.split('.'), self.fairy_instance.model

            for index, value in enumerate(field_list):
                field = model._meta.get_field(value)

                # 这里只有是关系字段才会处理，如果不是，则直接忽略
                if not meta.is_relation_field(field):
                    continue

                # 虚拟的关系字段
                if meta.is_virtual_relation_field(field):
                    # 如果是虚拟的关系字段，则使用祖宗名称，因为只有祖宗名称才能 prefetch_related
                    accessor_name = meta.get_accessor_name(field)
                    if accessor_name:
                        field_list[index] = accessor_name

                model = field.related_model
            result.append('.'.join(field_list))
        self.fairy_instance.transform_expand_fields = result


class FairyRetrieveModelMixin:
    """检索单个对象"""

    def fairy_connate_retrieve(self, request, *args, **kwargs):
        """原生的检索"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        获取数据详情
        """
        reset_handler = self.fairy_instance.custom_action_handler
        if reset_handler:
            return reset_handler(self, request, *args, **kwargs)

        return self.fairy_connate_retrieve(request, *args, **kwargs)


class FairyPostRetrieveModelMixin:
    """post 型的检索数据"""

    def fairy_connate_retrieve_enhance(self, request, *args, **kwargs):
        """原生的检索"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(serializer.data)

    @action(methods=['POST'], detail=True, url_path='retrieve')
    def retrieve_enhance(self, request, *args, **kwargs):
        reset_handler = self.fairy_instance.custom_action_handler
        if reset_handler:
            return reset_handler(self, request, *args, **kwargs)

        return self.fairy_connate_retrieve_enhance(request, *args, **kwargs)

    @action(methods=['POST'], detail=True, url_path='retrieve/mine')
    def retrieve_mine(self, request, *args, **kwargs):
        reset_handler = self.fairy_instance.custom_action_handler
        if reset_handler:
            return reset_handler(self, request, *args, **kwargs)

        return self.fairy_connate_retrieve_enhance(request, *args, **kwargs)


class FairyDestroyModelMixin:
    """
    删除一条指定的对象
    """

    def perform_destroy(self, instance):
        instance.delete()

    def fairy_connate_destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response()

    def destroy(self, request, *args, **kwargs):
        """
        删除数据
        """
        reset_handler = self.fairy_instance.custom_action_handler
        if reset_handler:
            return reset_handler(self, request, *args, **kwargs)
        return self.fairy_connate_destroy(request, *args, **kwargs)


class _BaseListMixin:
    """列表查询基类"""

    def _list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            return success_response(response.data)

        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)


class FairyListModelMixin(_BaseListMixin):
    """获取列表数据"""

    def list(self, request, *args, **kwargs):
        reset_handler = self.fairy_instance.custom_action_handler
        if reset_handler:
            return reset_handler(self, request, *args, **kwargs)
        return self._list(request, *args, **kwargs)


class FairyPostListModelMixin(_BaseListMixin):
    """POST 型获取列表"""

    @action(methods=['POST'], detail=False, url_path='list')
    def list_enhance(self, request, *args, **kwargs):
        """
        增强型的获取列表数据

        请求方法为：POST
        """
        reset_handler = self.fairy_instance.custom_action_handler
        if reset_handler:
            return reset_handler(self, request, *args, **kwargs)
        return self._list(request, *args, **kwargs)

    @action(methods=['POST'], detail=False, url_path='list/mine')
    def list_mine(self, request, *args, **kwargs):
        """
        增强型的专属针对当前登录用户获取列表数据

        请求方法为：POST
        """
        reset_handler = self.fairy_instance.custom_action_handler
        if reset_handler:
            return reset_handler(self, request, *args, **kwargs)
        return self._list(request, *args, **kwargs)


class FairyCreateModelMixin:
    """客户端的创建类"""

    def perform_create(self, serializer):
        return serializer.save()

    def fairy_connate_create(self, request, *args, **kwargs):
        data = request.data.get('data', {})
        with transaction.atomic():
            # 处理正向的关系数据
            fairy_pip_user_add_handle(self, data)
            serializer = self.get_validate_form(self.action)(data=data)
            serializer.is_valid(raise_exception=True)

            instance = self.perform_create(serializer)
            serializer = self.get_serializer(instance)
            return success_response(serializer.data)

    def create(self, request, *args, **kwargs):
        reset_handler = self.fairy_instance.custom_action_handler
        if reset_handler:
            return reset_handler(self, request, *args, **kwargs)
        return self.fairy_connate_create(request, *args, **kwargs)


class _BaseUpdateMixin:
    """更新动作基类"""

    def perform_update(self, serializer):
        return serializer.save()

    def _update(self, request, partial, *args, **kwargs):
        data = request.data.get('data', {})
        instance = self.get_object()

        with transaction.atomic():
            fairy_pip_user_add_handle(self, data)
            serializer = self.get_validate_form(self.action)(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            instance = self.perform_update(serializer)
            serializer = self.get_serializer(instance)
            return success_response(serializer.data)


class FairyUpdateModelMixin(_BaseUpdateMixin):
    """更新数据"""

    def update(self, request, *args, **kwargs):
        """全量更新数据"""
        reset_handler = self.fairy_instance.custom_action_handler
        if reset_handler:
            return reset_handler(self, request, *args, **kwargs)
        return self._update(request, False, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """部分字段更新"""
        reset_handler = self.fairy_instance.custom_action_handler
        if reset_handler:
            return reset_handler(self, request, *args, **kwargs)
        return self._update(request, True, *args, **kwargs)


class FairyPutPartialUpdateModelMixin(_BaseUpdateMixin):
    """put 型的部分更新

    因为有些端不支持或者不推荐使用 patch 方法
    """

    @action(methods=['put'], detail=True, url_path='patch')
    def patch_enhance(self, request, *args, **kwargs):
        reset_handler = self.fairy_instance.custom_action_handler
        if reset_handler:
            return reset_handler(self, request, *args, **kwargs)
        return self._update(request, True, *args, **kwargs)


class FairyCloudFuncMixin:
    """云函数"""

    @action(methods=['post'], detail=False, url_path='cloudfunc')
    def cloudfunc(self, request, *args, **kwargs):
        data = request.data.get('data')
        func_name = self.fairy_instance.request_namespace.get(const.FAIRY_CLIENT_CLOUD_FUNC_NAME)
        handler = self.fairy_instance.custom_action_handler

        if not handler:
            raise exception.FairySpaceException(
                error_code=exception.FAIRY_FUNCTION_NOT_FOUNT,
                error_data=f'找不到对应的云函数处理器：{func_name}',
            )

        result = handler(self, request, data, *args, **kwargs)
        return success_response(result)


class _BatchProcessForm(serializers.Serializer):
    """批量处理的验证表单"""

    func_name = serializers.CharField(max_length=50)
    data = serializers.ListField(min_length=1)

    def validate_func_name(self, value):
        view = self.context['view']
        self.batch_action = view.fairy_instance.custom_action_handler

        if not self.batch_action:
            raise exception.FairySpaceException(
                error_code=exception.FAIRY_PARAMETER_FORMAT_ERROR,
                error_data='传入的 action: {} 不支持'.format(value),
            )
        return value

    def validate_data(self, value):
        model = self.context.get('view').fairy_instance.model
        filter_params = {f'{model._meta.pk.name}__in': value}

        queryset = model.objects.filter(**filter_params)
        if len(value) != queryset.count():
            raise exception.FairySpaceException(
                error_code=exception.FAIRY_PARAMETER_BUSINESS_ERROR,
                error_message='列表中包含不合法 id 的数据',
            )
        self.batch_queryset = queryset
        return value

    def handle(self, view, request, *args, **kwargs):
        try:
            return self.batch_action(view, request, self.batch_queryset, *args, **kwargs)
        except Exception as e:
            raise exception.FairySpaceException(error_code=exception.FAIRY_BATCH_ACTION_HAND_ERROR, error_data=str(e))


class FairyBatchHandleMixin:
    """批量处理"""

    @action(methods=['post'], detail=False, url_path='batch')
    def batch(self, request, *args, **kwargs):
        """
        批量处理
        """
        data = {
            'data': request.data.get('data'),
            'func_name': self.fairy_instance.request_namespace.get(const.FAIRY_CLIENT_CLOUD_FUNC_NAME),
        }

        serializer = _BatchProcessForm(data=data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        response = serializer.handle(self, request, *args, **kwargs)
        return success_response(response)
