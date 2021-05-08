from django.urls import path
from .views import TimelineView

urlpatterns = [
    path('/comment',TimelineView.as_view()),
]