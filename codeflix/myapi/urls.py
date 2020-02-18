from django.urls import path

from . import views

urls = [
    path('api/', views.APIRoot.as_view(), name='api-root'),
    path('api/recommendation/<handle>/', views.RecommendedProblemView.as_view(), name='api-recommendation'),
]
