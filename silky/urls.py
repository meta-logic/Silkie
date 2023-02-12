"""jscoq URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from silky_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.startPage),
    path('upload/', views.uploadPage),
    path('test/', views.secondPage),
    path('test/1', views.q1),
    path('test/2', views.q2),
    path('test/3', views.q3),
    path('test/4', views.q4),
    path('test/submit', views.submit),
    path('help/', views.usagePage)
]
