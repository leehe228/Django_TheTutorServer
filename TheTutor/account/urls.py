from django.urls import path
from . import views

urlpatterns = [
    path('', views.account, name='account'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('sendFeedback/', views.sendFeedback, name='sendFeedback'),
    path('sendCode/', views.sendCode, name='sendCode'),
    path('changePassword/', views.changePassword, name='changePassword'),
    path('delete/', views.delete, name='delete'),
    path('userTime/', views.userTime, name='userTime'),
    path('getNotification/', views.getNotification, name='getNotification'),
    path('clearTime/', views.clearTime, name='clearTime'),
    path('updateTime/', views.updateTime, name='updateTime'),
    path('saveSub/', views.saveSub, name='saveSub'),
    path('loadSub/', views.loadSub, name='loadSub'),
    path('learn/', views.learn, name='learn'),
    path('goodMorning/', views.goodMorning, name='goodMorning'),
    path('saveTodo/', views.saveTodo, name='saveTodo'),
    path('loadTodo/', views.loadTodo, name='loadTodo')
]

