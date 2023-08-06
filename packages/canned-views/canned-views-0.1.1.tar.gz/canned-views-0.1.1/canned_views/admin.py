from django.contrib import admin
from django.template.loader import render_to_string
from django.urls import reverse

from .admin_site import canned_views_admin
from .auth_objects import CANNED_SUPER_ROLE
from .forms import CannedViewsForm
from .models import CannedViews


@admin.register(CannedViews, site=canned_views_admin)
class CannedViewsAdmin(admin.ModelAdmin):

    form = CannedViewsForm

    fieldsets = (
        (
            None,
            (
                {
                    "fields": (
                        "report_datetime",
                        "name",
                        "display_name",
                        "description",
                        "sql_view_name",
                    )
                }
            ),
        ),
    )

    list_display = [
        "display_name",
        "list_view",
        "description",
        "sql_view_name",
    ]

    search_fields = ("name", "display_name", "sql_view_name")

    readonly_fields = ["sql_view_name"]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj) or []
        if "sql_view_name" in readonly_fields and CANNED_SUPER_ROLE in [
            role.name for role in request.user.userprofile.roles.all()
        ]:
            readonly_fields.remove("sql_view_name")
        return readonly_fields

    @staticmethod
    def list_view(obj=None, label=None):
        url = reverse(
            "canned_views:basic_view_url",
            kwargs=dict(name=obj.name),
        )
        context = dict(title="Go to canned view", url=url, label=label)
        return render_to_string("canned_views/button.html", context=context)
