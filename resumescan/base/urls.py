from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('scan', views.scan, name="scan"),
    path('cvAnlys/<str:pk>/', views.analyseResume, name="analyseResume"),
]