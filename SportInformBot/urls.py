from django.conf.urls import url

from .views import CommandReceiveView

urlpatterns = [
    url(r'^bot/(?P<631895922:AAHrRowaIaY3OHB6KN6hw9fwKt02NMtz-LI>.+)/$', CommandReceiveView.as_view(), name='command'),
]
