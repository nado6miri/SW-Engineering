"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url

from photo.views import *

urlpatterns = [

    # Example: /
    url(r'^$', AlbumLV.as_view(), name='index'),

    # Example: /album/, same as /
    url(r'^album/$', AlbumLV.as_view(), name='album_list'),

    # Example: /album/99/
    url(r'^album/(?P<pk>\d+)/$', AlbumDV.as_view(), name='album_detail'),

    # Example: /photo/99/
    url(r'^photo/(?P<pk>\d+)/$', PhotoDV.as_view(), name='photo_detail'),

    # Example: /album/add/
    url(r'^album/add/$',
        AlbumPhotoCV.as_view(), name="album_add",
    ),

    # Example: /album/change/
    url(r'^album/change/$',
        AlbumChangeLV.as_view(), name="album_change",
    ),

    # Example: /album/99/update/
    url(r'^album/(?P<pk>[0-9]+)/update/$',
        AlbumPhotoUV.as_view(), name="album_update",
    ),

    # Example: /album/99/delete/
    url(r'^album/(?P<pk>[0-9]+)/delete/$',
        AlbumDeleteView.as_view(), name="album_delete",
    ),

    # Example: /photo/add/
    url(r'^photo/add/$',
        PhotoCreateView.as_view(), name="photo_add",
    ),

    # Example: /photo/change/
    url(r'^photo/change/$',
        PhotoChangeLV.as_view(), name="photo_change",
    ),

    # Example: /photo/99/update/
    url(r'^photo/(?P<pk>[0-9]+)/update/$',
        PhotoUpdateView.as_view(), name="photo_update",
    ),

    # Example: /photo/99/delete/
    url(r'^photo/(?P<pk>[0-9]+)/delete/$',
        PhotoDeleteView.as_view(), name="photo_delete",
    ),
]

