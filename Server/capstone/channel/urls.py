from django.urls import path
from .views import ChannelListView,CommentView

urlpatterns = [
    #path('/list', ChannelListView.as_view()),
    path('/comment',CommentView.as_view()),
]