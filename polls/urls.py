from django.urls import path

from . import views

urlpatterns = [
    # /
    path('', views.index, name='index'),
    # /5/
    path('<int:product_id>/', views.detail, name='detail'),
]