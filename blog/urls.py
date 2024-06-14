from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path(
        '',
        views.PostListView.as_view(),
        name='index'
    ),
    path('post/<slug:slug>/', views.post, name='post'),
    path('page/<slug:slug>/', views.page, name='page'),
    path(
        'created_by/<int:author_pk>/',
        views.CreatedByListView.as_view(),
        name='created_by'
    ),
    path('category/<slug:slug>/', views.category, name='category'),
    path('tag/<slug:slug>/', views.tag, name='tag'),
    path('search/', views.search, name='search'),
]
