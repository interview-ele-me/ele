from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import register

urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^login/$', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
]
