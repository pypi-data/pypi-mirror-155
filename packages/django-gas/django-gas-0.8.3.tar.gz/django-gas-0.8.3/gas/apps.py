from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GASConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'gas'
    verbose_name = _('GAS')

    def ready(self):
        from .sites import site
        super().ready()
        site.autodiscover()
