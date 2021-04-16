from django.urls import path
from .views import ChannelListView,CommentView

urlpatterns = [
    path('/subscribers', ChannelListView.as_view()),
    path('/comment/url',CommentView.as_view()),
]