from django.urls import path

from .views import *



app_name = 'blog'
urlpatterns = [

    # Example: /
    path('', PostLV.as_view(), name='index'),

    # Example: /post/ (same as /)
    path('post/', PostLV.as_view(), name='post_list'),

    # Example: /post/django-example/
    path('post/<slug:slug>/', PostDV.as_view(), name='post_detail'),

    # Example: /archive/
    path('archive/', PostAV.as_view(), name='post_archive'),

    # Example: /archive/2012/
    path('archive/<int:year>/', PostYAV.as_view(), name='post_year_archive'),

    # Example: /archive/2012/nov/
    path('archive/<int:year>/<str:month>/', PostMAV.as_view(), name='post_month_archive'),

    # Example: /archive/2012/nov/10/
    path('archive/<int:year>/<str:month>/<int:day>/', PostDAV.as_view(), name='post_day_archive'),

    # Example: /archive/today/
    path('archive/today/', PostTAV.as_view(), name='post_today_archive'),

    # Example: /tag/
    path('tag/', TagTV.as_view(), name='tag_cloud'),

    # Example: /tag/tagname/
    path('tag/<str:tag>/', PostTOL.as_view(), name='tagged_object_list'),

    # Example: /search/
    path('search/', SearchFormView.as_view(), name='search'),

    # Example: /add/
    path('add/',
         PostCreateView.as_view(), name="add",
    ),

    # Example: /change/
    path('change/',
         PostChangeLV.as_view(), name="change",
    ),

    # Example: /99/update/
    path('<int:pk>/update/',
         PostUpdateView.as_view(), name="update",
    ),

    # Example: /99/delete/
    path('<int:pk>/delete/',
         PostDeleteView.as_view(), name="delete",
    ),
]
