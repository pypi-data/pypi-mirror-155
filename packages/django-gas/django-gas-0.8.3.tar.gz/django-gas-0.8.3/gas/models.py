from django.db import models
from django.utils.translation import gettext_lazy as _

from gas.sites import site


class UserRole(models.Model):
    role = models.CharField(_('role'), max_length=150, choices=site.role_choices)
    user = models.ForeignKey(
        'auth.User', verbose_name=_('user'), related_name='user_roles',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('user role')
        verbose_name_plural = _('user roles')

    def __str__(self):
        return self.role

    @property
    def description(self):
        return site.get_role_description(self.role)
