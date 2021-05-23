from django.urls import path
from .views import KoreanView

urlpatterns = [

    path('/kr',KoreanView.as_view()),
]