"""codeflix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from myapi.urls import urls as myapi_urls

from . import settings, views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.UserCreateView.as_view(), name="signup"),
    path('accounts/activate/sent/', views.UserActivationEmailSentView.as_view(), name='account_activation_sent'),
    path('accounts/activate/<uidb64>/<token>/', views.UserActivateView.as_view(), name='account_activation'),
    path('accounts/<int:pk>/summary/', views.UserSummaryView.as_view(), name='account_summary'),
    path('accounts/<int:pk>/update/', views.UserUpdateView.as_view(), name='account_update'),
    path('accounts/<int:pk>/avatar/update/', views.AvatarUpdateView.as_view(), name='avatar_update'),
    path('accounts/<int:pk>/avatar/update/erase/', views.AvatarEraseView.as_view(), name='avatar_erase'),
    path('accounts/<int:pk>/codeforces/update/', views.CodeforcesUpdateView.as_view(), name='codeforces_update'),
    path('graph/dump/', views.DumpGraphView.as_view(), name='dump_graph'),
    path('graph/dump/done/', views.DumpGraphDoneView.as_view(), name='dump_graph_done'),
    path('graph/dump/failed/', views.DumpGraphFailedView.as_view(), name='dump_graph_failed'),
    path('graph/load/', views.LoadGraphView.as_view(), name='load_graph'),
    path('graph/load/done/', views.LoadGraphDoneView.as_view(), name='load_graph_done'),
    path('graph/load/failed/', views.LoadGraphFailedView.as_view(), name='load_graph_failed'),
    path('recommendation/<int:pk>/', views.RecommendationView.as_view(), name='recommendation'),
    path('recommendation/<int:pk>/renew_recommendation/', views.RenewRecommendationView.as_view(), name='renew_recommendation'),
    path('admin/', admin.site.urls),
    path('select2/', include('django_select2.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += myapi_urls
