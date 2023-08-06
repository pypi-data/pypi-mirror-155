from django import forms
from django.utils.translation import gettext_lazy as _

from gas.forms import BaseFilterForm
from gas.sites import site


class UserFilterForm(BaseFilterForm):
    username = forms.CharField(label=_('Username'), required=False)
    is_active = forms.NullBooleanField(label=_('Active'), required=False)
    roles = forms.MultipleChoiceField(
        label=_('Roles'), choices=site.role_choices, required=False,
    )

    def filter(self, qs):
        qs = super().filter(qs)

        username = self.cleaned_data['username']
        if username:
            qs = qs.filter(username__icontains=username)

        is_active = self.cleaned_data['is_active']
        if is_active is not None:
            qs = qs.filter(is_active=is_active)

        roles = self.cleaned_data['roles']
        if roles:
            qs = qs.filter(user_roles__role__in=roles)

        return qs
