from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from gas.sites import site


class BaseFilterForm(forms.Form):
    """
        Form for content filtering.

        The `filter` method must be replaced.
    """
    def filter(self, qs):
        """
            This function takes a queryset and returns another queryset, with
            the content filtered with the data in the form.
        """
        return qs


class UserForm(forms.ModelForm):
    roles = forms.MultipleChoiceField(
        choices=site.role_choices,
        label=_('roles'),
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'email', 'is_active',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk is not None:
            self.initial['roles'] = list(self.instance.user_roles.values_list('role', flat=True))

    def save(self, commit=True):
        obj = super().save(commit=False)

        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            roles = self.cleaned_data['roles']
            for role in roles:
                obj.user_roles.update_or_create(role=role)
            obj.user_roles.exclude(role__in=roles).delete()

        self.save_m2m = save_m2m

        if commit:
            obj.save()
            self.save_m2m()

        return obj


def split_datetime_field(form, field_name):
    old_field = form.fields[field_name]
    new_field = forms.SplitDateTimeField(
        label=old_field.label,
        label_suffix=old_field.label_suffix,
        required=old_field.required,
        help_text=old_field.help_text,
        initial=old_field.initial,
        validators=old_field.validators,
        localize=old_field.localize,
        disabled=old_field.disabled,
        input_date_formats=("%Y-%m-%d",),
        input_time_formats=("%H:%M", "%H:%M:%S"),
        widget=forms.SplitDateTimeWidget(
            date_format='%Y-%m-%d',
            time_format='%H:%M:%S',
            time_attrs={'placeholder': '00:00'},
        ),
    )
    new_field.widget.widgets[0].input_type = 'date'
    form.fields[field_name] = new_field
