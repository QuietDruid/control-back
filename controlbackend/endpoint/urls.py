from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="test_index"),
    path('api/classes/', views.create_class, name='create_class'),
    path('api/classes/list/', views.get_classes, name='get_classes'),
]
