import json
import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory
from django.views.generic import View, FormView, TemplateView
from django.contrib import messages
from django.contrib.messages.storage import default_storage

from model_bakery import baker

from gas import views as gviews
from gas import gas_settings
from gas.forms import UserForm
from gas.gas.users.views import UserList


class AjaxCommandTestCase(TestCase):
    def test_ajaxcommands_view(self):
        class SampleAjaxView(gviews.AjaxCommandsMixin, View):
            def do_test(self):
                return self.render_json({'success': True})

        class SampleForm(forms.Form):
            field = forms.CharField()

        class SampleAjaxWithPostView(gviews.AjaxCommandsMixin, FormView):
            form_class = SampleForm

            def render_to_response(self, context, **response_kwargs):
                return HttpResponse("OK")

            def form_valid(self, form):
                return self.form_invalid(form)

        view = SampleAjaxView.as_view()
        post_view = SampleAjaxWithPostView.as_view()
        request_factory = RequestFactory()

        # Command with corresponding "do_" method
        request = request_factory.post('some_url', {
            'command': 'test',
        })
        response = view(request)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertTrue(data['success'])

        # Command with no corresponding "do_" method returns BadRequest
        request = request_factory.post('some_url', {
            'command': 'missing_test',
        })
        response = view(request)
        self.assertEqual(response.status_code, 400)  # Bad Request

        # With no command process normal POST request
        request = request_factory.post('some_url', {
            'not_command': 'test',
        })
        response = view(request)
        self.assertEqual(response.status_code, 405)  # Not Allowed
        request = request_factory.post('some_url', {
            'field': 'test',
        })
        response = post_view(request)
        self.assertEqual(response.status_code, 200)

    def test_custom_json_encoder(self):
        class CustomEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, datetime.datetime):
                    return 'datetime'
                if isinstance(obj, datetime.date):
                    return 'date'
                return json.JSONEncoder.default(self, obj)

        class SampleAjaxView(gviews.AjaxCommandsMixin, View):
            def do_test(self):
                return self.render_json({
                    'now': datetime.datetime.now(),
                    'today': datetime.date.today(),
                }, encoder=CustomEncoder)

        view = SampleAjaxView.as_view()
        request_factory = RequestFactory()

        # Command with corresponding "do_" method
        request = request_factory.post('some_url', {
            'command': 'test',
        })
        response = view(request)
        data = json.loads(response.content)
        self.assertEqual(data['now'], 'datetime')
        self.assertEqual(data['today'], 'date')


class GASMixinTestCase(TestCase):
    def setUp(self):
        self.admin_user = baker.make(
            'auth.User',
            is_superuser=True,
        )
        self.admin_role_user = baker.make(
            'auth.User',
            user_roles__role='admins'
        )
        self.staff_role_user = baker.make(
            'auth.User',
            user_roles__role='staff'
        )
        self.no_role_user = baker.make(
            'auth.User',
            is_superuser=False,
        )
        self.request_factory = RequestFactory()

    def test_dispatch(self):
        class SampleView(gviews.GASMixin, View):
            """
                GAS default authentication, allowed superusers and users
                with admins role.
            """
            def get(self, request, *args, **kwargs):
                return HttpResponse("OK")

        view = SampleView.as_view()
        request = self.request_factory.get('some_url')

        # superusers allowed
        request.user = self.admin_user
        response = view(request)
        self.assertEqual(response.status_code, 200)

        # admins role allowed
        request.user = self.admin_role_user
        response = view(request)
        self.assertEqual(response.status_code, 200)

        # others not allowed
        request.user = self.no_role_user
        response = view(request)
        self.assertEqual(response.status_code, 302)
        request.user = self.staff_role_user
        response = view(request)
        self.assertEqual(response.status_code, 302)

        class SampleStaffView(gviews.GASMixin, View):
            """
                Allowed superusers and users with admins and staff roles.
            """
            roles = ('staff',)

            def get(self, request, *args, **kwargs):
                return HttpResponse("OK")

        view = SampleStaffView.as_view()
        request = self.request_factory.get('some_url')

        # superusers allowed
        request.user = self.admin_user
        response = view(request)
        self.assertEqual(response.status_code, 200)

        # admins role allowed
        request.user = self.admin_role_user
        response = view(request)
        self.assertEqual(response.status_code, 200)

        # staff role allowed
        request.user = self.staff_role_user
        response = view(request)
        self.assertEqual(response.status_code, 200)

        # others not allowed
        request.user = self.no_role_user
        response = view(request)
        self.assertEqual(response.status_code, 302)

    def test_form_valid(self):
        class SampleForm(forms.Form):
            field = forms.CharField()

        class SampleFormView(gviews.GASMixin, FormView):
            form_class = SampleForm
            success_message = 'success message'
            continue_url = 'continue'
            success_url = 'success'

        view = SampleFormView.as_view()

        # Normal workflow
        request = self.request_factory.post('some_url', {
            'field': 'test',
        })
        request.user = self.admin_user
        request._messages = default_storage(request)
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'success')
        msgs = [
            (m.level, m.message)
            for m in messages.get_messages(request)
        ]
        self.assertIn((messages.SUCCESS, 'success message'), msgs)

        # Save and continue
        request = self.request_factory.post('some_url', {
            'field': 'test',
            'save_and_continue': '1',
        })
        request.user = self.admin_user
        request._messages = default_storage(request)
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'continue')

    def test_context_data(self):
        class SampleView(gviews.GASMixin, TemplateView):
            title = 'title'
            header_title = 'header title'
            help_text = 'help text'
            breadcrumbs = [
                ('url', 'label'),
            ]
            template_name = 'gas/base.html'

        view = SampleView.as_view()
        request = self.request_factory.get('some_url')
        request.user = self.admin_user
        response = view(request)
        self.assertEqual(response.context_data['title'], SampleView.title)
        self.assertEqual(response.context_data['header_title'], SampleView.header_title)
        self.assertEqual(response.context_data['help_text'], SampleView.help_text)
        self.assertEqual(response.context_data['base_template'], SampleView.base_template)
        self.assertEqual(response.context_data['breadcrumbs'], SampleView.breadcrumbs)
        self.assertEqual(response.context_data['gas_title'], gas_settings.TITLE)
        self.assertEqual(response.context_data['logo_static_url'], gas_settings.LOGO)
        self.assertEqual(response.context_data['css'], gas_settings.MEDIA['css'])
        self.assertEqual(response.context_data['js'], gas_settings.MEDIA['js'])

    def test_no_header_title(self):
        class NoHeaderTitleSampleView(gviews.GASMixin, TemplateView):
            title = 'title'
            template_name = 'gas/base.html'

        view = NoHeaderTitleSampleView.as_view()
        request = self.request_factory.get('some_url')
        request.user = self.admin_user
        response = view(request)
        self.assertEqual(response.context_data['title'], NoHeaderTitleSampleView.title)
        self.assertEqual(response.context_data['header_title'], NoHeaderTitleSampleView.title)

        # test error with save_and_continue and no continue_url
        class SampleForm(forms.Form):
            field = forms.CharField()

        class NoContinueUrlSampleView(gviews.GASMixin, FormView):
            form_class = SampleForm
            success_url = 'success'

        view = NoContinueUrlSampleView.as_view()
        request = self.request_factory.post('some_url', {
            'field': 'test',
            'save_and_continue': '1',
        })
        request.user = self.admin_user

        with self.assertRaises(ImproperlyConfigured):
            response = view(request)

    def test_extra_css(self):
        class SampleView(gviews.GASMixin, TemplateView):
            template_name = 'test.html'

        view = SampleView.as_view()
        request = self.request_factory.get('some_url')

        request.user = self.admin_user
        response = view(request)
        self.assertEqual(response.status_code, 200)

        gas_settings.EXTRA_MEDIA = None
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('test.css', response.context_data['css'])
        self.assertNotIn('test.js', response.context_data['js'])

        gas_settings.EXTRA_MEDIA = {'css': ['test.css']}
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('test.css', response.context_data['css'])
        self.assertNotIn('test.js', response.context_data['js'])

        gas_settings.EXTRA_MEDIA = {'js': ['test.js']}
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('test.css', response.context_data['css'])
        self.assertIn('test.js', response.context_data['js'])

        gas_settings.EXTRA_MEDIA = {'css': ['test.css'], 'js': ['test.js']}
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('test.css', response.context_data['css'])
        self.assertIn('test.js', response.context_data['js'])


class GASListTestCase(TestCase):
    def test_filtered(self):
        request_factory = RequestFactory()

        baker.make(
            'auth.User', username='testuser',
            user_roles__role='staff'
        )
        admin_user = baker.make(
            'auth.User',
            username='anothertestuser',
            user_roles__role='admins',
            is_superuser=True,
        )
        baker.make('auth.User', username='anotherone')

        view = UserList.as_view()

        # default listing with all users
        request = request_factory.get('some_url')
        request.user = admin_user
        response = view(request)
        self.assertEqual(response.context_data['user_list'].count(), 3)

        # filter by username
        request = request_factory.get('some_url', {
            'username': 'test',
        })
        request.user = admin_user
        response = view(request)
        self.assertEqual(response.context_data['user_list'].count(), 2)

        # filter by roles
        request = request_factory.get('some_url', {
            'roles': ['staff'],
        })
        request.user = admin_user
        response = view(request)
        self.assertEqual(response.context_data['user_list'].count(), 1)

        # filter_form_class not required
        class NotFiltered(gviews.GASListView):
            model = User

        view = NotFiltered.as_view()
        request = request_factory.get('some_url')
        request.user = admin_user
        response = view(request)
        self.assertEqual(response.context_data['user_list'].count(), 3)


class GASCreateTestCase(TestCase):
    def test_popup(self):
        request_factory = RequestFactory()

        admin_user = baker.make(
            'auth.User',
            username='admin',
            is_superuser=True,
        )

        class SampleCreateView(gviews.GASCreateView):
            model = User
            form_class = UserForm
            success_url = 'success'

        view = SampleCreateView.as_view()

        # returning from popup
        request = request_factory.post('some_url', {
            '_popup': '1',

            'username': 'testuser',
            'first_name': 'test',
            'last_name': 'user',
            'email': 'email@example.org',
            'is_active': '1',
        })
        request.user = admin_user
        request._messages = default_storage(request)
        response = view(request)
        self.assertIn(b'dismissAddAnotherPopup', response.content)

        # normal workflow, redirect to success_url
        request = request_factory.post('some_url', {
            'username': 'testuser2',
            'first_name': 'test2',
            'last_name': 'user2',
            'email': 'email2@example.org',
            'is_active': '1',
        })
        request.user = admin_user
        request._messages = default_storage(request)
        response = view(request)
        self.assertEqual(response.status_code, 302)

        # is_popup on context_data
        request = request_factory.get('some_url', {
            '_popup': '1',
        })
        request.user = admin_user
        response = view(request)
        self.assertEqual(response.context_data['is_popup'], True)


class GASDeleteTestCase(TestCase):
    def test_context_data(self):
        request_factory = RequestFactory()
        user = baker.make(User, username='testuser')
        admin_user = baker.make(
            'auth.User',
            username='admin',
            is_superuser=True,
        )

        class SampleDeleteView(gviews.GASDeleteView):
            model = User
            success_url = 'success'
            confirmation_text = 'delete {object.username}'
            deleted_text = '{object.username} deleted'
        
        view = SampleDeleteView.as_view()

        request = request_factory.get('some_url')
        request.user = admin_user
        response = view(request, pk=user.pk)
        ctx = response.context_data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ctx['confirmation_text'], 'delete testuser')
        self.assertEqual(response.context_data['cancel_url'], 'success')
        self.assertEqual(len(ctx['deleted_objects']), 1)
        self.assertEqual(ctx['deleted_model_count']['users'], 1)

        request = request_factory.post('some_url', pk=user.pk)
        request.user = admin_user
        request._messages = default_storage(request)
        response = view(request, pk=user.pk)

        self.assertEqual(response.status_code, 302)
        msgs = [
            (m.level, m.message)
            for m in messages.get_messages(request)
        ]
        self.assertIn((messages.SUCCESS, 'testuser deleted'), msgs)
