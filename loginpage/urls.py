from django.urls import path
from jackfruit import views


urlpatterns = [
    path('del', views.DeleteData.as_view()),
    path('get', views.GetData.as_view()),
    path('manage', views.ManageData.as_view()),
    path('regi', views.Register.as_view()),
    path('up',views.Update.as_view()),
    path('login', views.Login.as_view())
]
