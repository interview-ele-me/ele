from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from lottery.views_api import buy, get_lucky_num, init_CountUserByPrize


urlpatterns = [
    url(r'^buy/$', buy),
    url(r'^get_lucky_num/$', get_lucky_num),
    url(r'^init_CountUserByPrize/$', init_CountUserByPrize),
]

urlpatterns = format_suffix_patterns(urlpatterns)
