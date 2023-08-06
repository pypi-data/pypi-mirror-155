from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.views.generic import ListView
from edc_dashboard.view_mixins import EdcViewMixin
from edc_navbar import NavbarViewMixin

from ..models import CannedViews
from ..utils import DynamicModel, DynamicModelError


class CannedViewNameError(Exception):
    pass


class BasicView(EdcViewMixin, NavbarViewMixin, ListView):
    queryset = None
    paginate_by = 100
    template_name = "canned_views/canned_view.html"
    navbar_selected_item = "canned_views"

    def __init__(self, **kwargs):
        self.report = None
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admin_url = reverse("canned_views_admin:canned_views_cannedviews_changelist")
        context.update(admin_url=f"{admin_url}?q={self.report.name}", report=self.report)
        return context

    def get(self, request, *args, name=None, **kwargs):
        try:
            self.report = CannedViews.objects.get(name=name)
        except ObjectDoesNotExist as e:
            raise CannedViewNameError(e)
        try:
            dynamic_model = DynamicModel(name, self.report.sql_view_name)
        except DynamicModelError as e:
            raise CannedViewNameError(e)
        self.model = dynamic_model.model_cls
        self.queryset = self.model.objects.raw(dynamic_model.sql)
        return super().get(request, *args, **kwargs)
