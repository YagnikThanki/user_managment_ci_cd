from django.urls import path
from .views import Registerview, register_view,login_view,register_list_view,logout_view,change_password,send_otp,confirmation_otp,forgot_password
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('register/', register_view,name='register'),
    path('login/', login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('change_password/',change_password,name='change_password'),
    path('send_otp/',send_otp,name='send_otp'),
    path('confirmation_otp/',confirmation_otp,name='confirmation_otp'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('register_api/', Registerview.as_view()),
    path('list/',register_list_view.as_view(),name='register api list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]   

