from django.conf.urls import url
from third_app import views


#template tagging

app_name= 'third_app'
urlpatterns=[
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/', views.user_login, name="user_login")
]