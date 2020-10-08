from . import views
from django.urls.conf import include
from django.conf.urls import url

urlpatterns = [
    url('kobe.html/', views.kobe, name='kobe_page')
]