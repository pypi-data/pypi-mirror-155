from django.conf import settings
from edc_navbar import Navbar, NavbarItem, site_navbars

no_url_namespace = True if settings.APP_NAME == "canned_views" else False

navbar_item = NavbarItem(
    name="canned_views_home",
    title="Monitoring Reports",
    label="MR",
    codename="edc_navbar.nav_canned_views_section",
    url_name="canned_views:home_url",
    no_url_namespace=no_url_namespace,
)

navbar = Navbar(name="canned_views")
navbar.append_item(navbar_item)

site_navbars.register(navbar)
