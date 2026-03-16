from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<str:cat_code>/', views.category_view, name='category'),
]

