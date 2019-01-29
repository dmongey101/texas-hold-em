"""django_blog URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf import settings
from poker.views import show_index
from accounts.views import signup
from donations.views import donations
from poker import urls as poker_urls
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
    path('poker/', include(poker_urls)),
    path('', show_index, name='index'),
    path('donations/pay/', donations, name='pay'),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]

handler404 = 'poker.views.error_404_view'