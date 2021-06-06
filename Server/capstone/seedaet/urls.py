from django.urls import path
from .views import SeeDaetView

urlpatterns = [
    #path('/list', ChannelListView.as_view()),
    path('daet',SeeDaetView.as_view()),
]