from django.urls import path
from .views import KoreanView, SpamView

urlpatterns = [

    path('/kr',KoreanView.as_view()),
    path('/spam',SpamView.as_view()),
]