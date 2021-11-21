from django.urls import path

from snippet.views import SnippetViewSet, TagViewSet

urlpatterns = [
    path('snippet/', SnippetViewSet.as_view({
        'post': 'create',
        'get': 'overview'
    })),
    path('snippet/<int:pk>/', SnippetViewSet.as_view({
        'patch': 'update',
        'get': 'retrive',
        'delete': 'destroy'
    }), name='snippet'),
    path('tag/', TagViewSet.as_view({
        'get': 'overview'
    })),
    path('tag/<int:pk>/', TagViewSet.as_view({
        'get': 'retrive'
    }))
]