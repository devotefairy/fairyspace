from rest_framework.routers import DynamicRoute, Route, SimpleRouter as OriginSimpleRouter


class SimpleRouter(OriginSimpleRouter):
    def __init__(self, **kwargs):

        self.fairy_base_name = kwargs.pop('fairy_base_name')
        super(SimpleRouter, self).__init__(**kwargs)

    def get_default_basename(self, viewset):
        """
        如果 base_name 没有指定，尝试从 viewset 自动获取
        """

        queryset = getattr(viewset, 'queryset', None)

        if queryset is None:
            return self.fairy_base_name

        return queryset.model._meta.object_name.lower()

    def get_default_base_name(self, viewset):
        """
        应对低版本的 DRF
        """
        return self.get_default_basename(viewset)


class FairySimpleRouter(SimpleRouter):

    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={'get': 'list', 'post': 'create'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'},
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$', name='{basename}-{url_name}', detail=False, initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'},
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={},
        ),
    ]


class FairyUploadRouter(SimpleRouter):

    routes = [
        # 上传文件
        Route(
            url=r'^{prefix}/upload{trailing_slash}$',
            mapping={'post': 'upload'},
            name='{basename}-upload',
            detail=False,
            initkwargs={'suffix': 'Upload'},
        ),
    ]
