from django.urls import path

from .views import *



app_name = 'bookmark'
urlpatterns = [
    path('', BookmarkLV.as_view(), name='index'),
    path('<int:pk>/', BookmarkDV.as_view(), name='detail'),

    # Example: /add/
    path('add/',
         BookmarkCreateView.as_view(), name="add",
    ),

    # Example: /change/
    path('change/',
         BookmarkChangeLV.as_view(), name="change",
    ),

    # Example: /99/update/
    path('<int:pk>/update/',
         BookmarkUpdateView.as_view(), name="update",
    ),

    # Example: /99/delete/
    path('<int:pk>/delete/',
         BookmarkDeleteView.as_view(), name="delete",
    ),
]
