from django.urls.conf import path

from .views import BasicView, HomeView

app_name = "canned_views"

urlpatterns = [
    path("canned_views/<name>/", BasicView.as_view(), name="basic_view_url"),
    path("", HomeView.as_view(), name="home_url"),
]
