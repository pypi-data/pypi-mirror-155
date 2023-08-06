from django.core.validators import RegexValidator
from django.db import models
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow


class CannedViews(SiteModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(default=get_utcnow)

    name = models.CharField(max_length=30, validators=[RegexValidator(regex="^([a-z_])+$")])

    display_name = models.CharField(max_length=30)

    description = models.TextField(null=True)

    sql_view_name = models.CharField(
        max_length=50,
        null=True,
        blank=False,
        validators=[RegexValidator(regex="^([a-z_])+$")],
    )

    objects = models.Manager()

    history = HistoricalRecords()

    sites = CurrentSiteManager()

    def __str__(self):
        return self.name

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Canned View"
        verbose_name_plural = "Canned Views"
