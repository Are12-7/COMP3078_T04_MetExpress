import imp
from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.registerUser, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('profile/<str:id>/', views.profilePage, name='user-profile'),
    path('', views.home, name="home"),
    path('village/<str:id>/', views.village, name="village"),
    path('debates/', views.debatesPage, name="debates"),
    path('create-village', views.createVillage, name="create-village"),
    path('update-village/<str:id>/', views.updateVillage, name="update-village"),
    path('delete-village/<str:id>/', views.deleteVillage, name="delete-village"),
    path('delete-discussion/<str:id>/',
         views.deleteDiscussion, name="delete-discussion"),
    path('discussions/', views.discussionsPage, name="discussions"),
    path('update-profile/', views.updateProfile, name="update-profile")
]
