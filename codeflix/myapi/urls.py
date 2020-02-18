from django.urls import path

from .views import RecommendedProblemView

urls = [
    path('api/recommendation/<handle>/', RecommendedProblemView.as_view(), name='api-recommendation'),
]
