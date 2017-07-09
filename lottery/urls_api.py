from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from lottery.views_api import buy, get_lucky_num


urlpatterns = [
    url(r'^buy/$', buy),
    url(r'^get_lucky_num/$', get_lucky_num),
]

urlpatterns = format_suffix_patterns(urlpatterns)
