from django.urls import reverse
from django.views.generic import TemplateView
from edc_dashboard.view_mixins import EdcViewMixin, UrlRequestContextMixin
from edc_navbar import NavbarViewMixin

from canned_views.models import CannedViews


class HomeView(UrlRequestContextMixin, EdcViewMixin, NavbarViewMixin, TemplateView):

    navbar_selected_item = "canned_views_home"
    template_name = "canned_views/home.html"
    url_name = "home_url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        reports = CannedViews.objects.all().order_by("name")
        home_url = reverse(self.url_name)
        context.update(reports=reports, home_url=home_url)
        return context
