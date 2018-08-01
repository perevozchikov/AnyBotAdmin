from django.conf.urls import url

from .views import command_start

urlpatterns = [
    url(r'^bot/(?P<bot_token>.+)/$', command_start, name='command'),
]
