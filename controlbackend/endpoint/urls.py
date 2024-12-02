from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

urlpatterns = [
    path('', views.index, name="test_index"),
    path('api/classes/', views.create_class, name='create_class'),
    path('api/classes/list/', views.get_classes, name='get_classes'),
    path('api/login/', views.login, name='login'),
    path('api/signup/', views.signup, name='signup'),
    path('api/test', views.test, name='test'),
]
