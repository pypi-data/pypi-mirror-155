from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView

from ..models import CannedViews
from ..utils import DynamicModel, DynamicModelError


class CannedViewNameError(Exception):
    pass


class BasicView(ListView):
    queryset = None
    paginate_by = 100
    template_name = "canned_view.html"

    def get(self, request, *args, name=None, **kwargs):
        try:
            reports = CannedViews.objects.get(name=name)
        except ObjectDoesNotExist as e:
            raise CannedViewNameError(e)
        try:
            dynamic_model = DynamicModel(name, reports.sql_view_name)
        except DynamicModelError as e:
            raise CannedViewNameError(e)
        self.model = dynamic_model.model_cls
        self.queryset = self.model.objects.raw(dynamic_model.sql)
        return super().get(request, *args, **kwargs)
