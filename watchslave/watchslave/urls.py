"""watchslave URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from check.views import run_ping,get_ping_logs,loading_test,max_user_count
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ping', run_ping),
    url(r'^get_logs',get_ping_logs),
    url(r'^load',loading_test),
    url(r'^max_conn',max_user_count)
]

