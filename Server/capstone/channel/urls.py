from django.urls import path
from .views import ChannelListView#,HistoryView

urlpatterns = [
    path('/subscribers', ChannelListView.as_view()),
    #path('/history',HistoryView()),
]