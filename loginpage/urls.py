from django.urls import path
from jackfruit import views


urlpatterns = [
    path('del', views.deleteData.as_view()),
    path('newone', views.getdata.as_view()),
    path('manage', views.managdata.as_view()),
    path('regi', views.Register.as_view()),
    path('up',views.update.as_view()),
    path('esra', views.login.as_view())
]
