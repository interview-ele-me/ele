from django.conf.urls import url
from lottery.views import index, result
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^index/$', index, name='index'),
    url(r'^result/(?P<prize_id>\d+)$', result, name='result'),
]
