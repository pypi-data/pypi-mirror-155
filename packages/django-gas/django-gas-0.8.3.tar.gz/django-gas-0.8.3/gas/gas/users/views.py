from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import FormView
from django.urls import reverse, reverse_lazy

from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

import gas.views as gviews
from gas.forms import UserForm

from .forms import UserFilterForm


class BaseMixin:
    model = User
    form_class = UserForm
    filter_form_class = UserFilterForm
    roles = ('admins',)

    def get_success_url(self):
        return reverse('gas:user_list')

    def get_continue_url(self):
        return reverse('gas:user_update', kwargs={'pk': self.object.pk})


class UserList(BaseMixin, gviews.GASListView):
    template_name = 'gas/users/user_list.html'
    title = _('Users')
    help_text = _('Manage users and set roles.')
    actions = [
        (reverse_lazy('gas:user_create'), 'fa-plus', _('New user')),
    ]

    def get_breadcrumbs(self):
        return (
            (None, _('Users')),
        )


class CreateUser(BaseMixin, gviews.GASCreateView):
    title = _('Create user')
    success_message = _('User created')

    def get_breadcrumbs(self):
        return (
            (reverse('gas:user_list'), _('Users')),
            (None, _('Create')),
        )


class UpdateUser(BaseMixin, gviews.GASUpdateView):
    title = _('Update user')
    success_message = _('User updated')

    def get_breadcrumbs(self):
        return (
            (reverse('gas:user_list'), _('Users')),
            (reverse('gas:user_update', args=(self.object.pk,)), self.object.username),
            (None, _('Update')),
        )


class ChangePasswordUser(BaseMixin, gviews.GASMixin, FormView):
    template_name = 'gas/base_form.html'
    form_class = AdminPasswordChangeForm
    success_message = _('User password updated')

    @cached_property
    def user(self):
        return get_object_or_404(User, pk=self.kwargs['pk'])

    def get_title(self):
        return _('Change {username} user password').format(username=self.user.username)

    def get_continue_url(self):
        return reverse('gas:user_change_password', args=(self.kwargs['pk'],))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'target_user': self.user,
        })
        return ctx

    def get_breadcrumbs(self):
        return (
            (reverse('gas:user_list'), _('Users')),
            (reverse('gas:user_update', args=(self.user.pk,)), self.user.username),
            (None, _('Change password')),
        )


class DeleteUser(BaseMixin, gviews.GASDeleteView):
    title = _('Delete user')
    success_message = _('User deleted')

    def get_breadcrumbs(self):
        return (
            (reverse('gas:user_list'), _('Users')),
            (reverse('gas:user_update', args=(self.object.pk,)), self.object.username),
            (None, _('Delete')),
        )
