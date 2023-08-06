from django.urls.conf import path
from django.views.generic import RedirectView

from .views import BasicView

app_name = "canned_views"

urlpatterns = [
    path("canned_views/<name>/", BasicView.as_view(), name="basic_view_url"),
    path("", RedirectView.as_view(url=f"/{app_name}/admin/"), name="home_url"),
]
