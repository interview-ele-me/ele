from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from lottery.views_api import buy


urlpatterns = [
    url(r'^buy/$', buy),
]

urlpatterns = format_suffix_patterns(urlpatterns)
