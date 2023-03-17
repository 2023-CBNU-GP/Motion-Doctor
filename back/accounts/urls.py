from . import views
from django.urls import path

urlpatterns = [
  path('signup', views.RegisterView.as_view()),
  path('login', views.LoginView.as_view()),
  path('user', views.UserView.as_view()),
  path('logout', views.LogoutView.as_view()),
  path('id_check', views.OverlabId.as_view()),
  path('email_check', views.EmailView.as_view()),
  path('code_check', views.EmailCodeView.as_view()),
  path('withdraw', views.UserDrop.as_view()),
  path('modifypw', views.PasswordModify.as_view())
]
