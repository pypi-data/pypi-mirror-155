from django import forms
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from .models import CannedViews


class CannedViewsForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = None

    class Meta:
        model = CannedViews
        fields = "__all__"
