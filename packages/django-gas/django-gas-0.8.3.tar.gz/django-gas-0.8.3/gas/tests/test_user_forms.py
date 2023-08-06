from django.contrib.auth.models import User
from django.test import TestCase

from model_bakery import baker

from gas import forms
from gas.gas.users import forms as user_forms


class UserFormsTestCase(TestCase):
    def test_user_form(self):
        user = baker.make('auth.User', first_name='name')
        data = {
            'first_name': 'changed name',
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'roles': ['staff',],
        }
        form = forms.UserForm(instance=user, data=data)
        self.assertTrue(form.is_valid())
        new_user = form.save()
        self.assertEqual(new_user.email, user.email)
        self.assertEqual(new_user.first_name, 'changed name')
        self.assertTrue(
            new_user.user_roles.filter(role='staff').exists()
        )
        self.assertFalse(
            new_user.user_roles.filter(role='admins').exists()
        )


class UserFilterFormTestCase(TestCase):
    def test_filter_form(self):
        user = baker.make(User,
            username='testname',
            user_roles__role='staff',
            is_active=True,
        )
        users = User.objects.all()
        
        # filter by username with match
        data = {
            'username': 'test',
        }
        form = user_forms.UserFilterForm(data)
        self.assertTrue(form.is_valid())
        user_in_queryset = form.filter(users).filter(pk=user.id).exists()
        self.assertTrue(user_in_queryset)

        # filter by username without match
        data = {
            'username': 'nonexistant',
        }
        form = user_forms.UserFilterForm(data)
        self.assertTrue(form.is_valid())
        user_in_queryset = form.filter(users).filter(pk=user.id).exists()
        self.assertFalse(user_in_queryset)

        # filter by is_active with match
        data = {
            'is_active': 'true',
        }
        form = user_forms.UserFilterForm(data)
        self.assertTrue(form.is_valid())
        user_in_queryset = form.filter(users).filter(pk=user.id).exists()
        self.assertTrue(user_in_queryset)

        # filter by is_active without match
        data = {
            'is_active': 'false',
        }
        form = user_forms.UserFilterForm(data)
        self.assertTrue(form.is_valid())
        filtered_qs = form.filter(users)
        user_in_queryset = form.filter(users).filter(pk=user.id).exists()
        self.assertFalse(user_in_queryset)

        # filter by role without match
        data = {
            'roles': ['admins'],
        }
        form = user_forms.UserFilterForm(data)
        self.assertTrue(form.is_valid())
        user_in_queryset = form.filter(users).filter(pk=user.id).exists()
        self.assertFalse(user_in_queryset)
