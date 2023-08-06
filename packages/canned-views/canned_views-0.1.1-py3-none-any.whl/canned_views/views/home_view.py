from django.conf import settings
from django.views.generic import TemplateView
from edc_dashboard.view_mixins import EdcViewMixin, UrlRequestContextMixin
from edc_navbar import NavbarViewMixin

from canned_views.models import CannedViews


class HomeView(UrlRequestContextMixin, EdcViewMixin, NavbarViewMixin, TemplateView):

    navbar_selected_item = "canned_views_home"
    template_name = f"canned_views/home.html"
    url_name = "home_url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        reports = CannedViews.objects.all().order_by("name")
        # context = self.add_url_to_context(
        #     new_key="home_url", existing_key=self.url_name, context=context
        # )
        context.update(reports=reports)
        return context
