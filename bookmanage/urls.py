from django.urls import path
from bookmanage import views

app_name = 'bookmanage'

urlpatterns = [
    path('', views.LoginView.as_view(),name='top'),
    path('login', views.LoginView.as_view(),name='login'),
    path('register', views.RegisterView.as_view(),name='register'),
    path('registerajax', views.RegisterView.as_view(),name='registerajax'),
    path('mypage', views.MypageView.as_view(),name='mypage'),
    path('mypageajax', views.MypageRenewView.as_view(),name='mypageajax'),
    path('bookregistajax', views.BookRegistView.as_view(),name='bookregistajax'),
]