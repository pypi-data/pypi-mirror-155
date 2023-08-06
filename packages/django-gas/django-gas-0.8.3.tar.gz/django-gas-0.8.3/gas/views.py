import json

from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.core.exceptions import ImproperlyConfigured
from django.db import router
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.utils.html import escape, escapejs
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from . import gas_settings
from . import utils


class AjaxCommandsMixin:
    """
        Mixin class for views with javascript interaction.

        Allows defining several commands (POST or GET) on a diferent
        method per command. A request is identified as a command if it has
        a `command` field in the request.

        To react to a POST command define a method starting  with `do_`.
        For example a request with a command named `store_answer` will be
        processed in the method `do_store_answer`.

        Similarly, to react to a GET command define a method starting with
        `send_`.  For example a request with a command named `user_list` will be
        processed in the method `send_user_list`.

        If the request has no command then it will be processed like in
        any other DJango view.

        If the request has a command not defined in the view it will get a
        400 response (Bad Request).

        The helper `render_json` method allows returning an
        application/json with automatic serialization of the given python
        data. It uses the extended json encoder allowing serialization of
        queryets, lazy strings, dates, etc.
    """
    def post(self, request, *args, **kwargs):
        if 'command' in self.request.POST:
            command_processor = getattr(self, 'do_{0}'.format(self.request.POST['command']), None)
            if command_processor is not None:
                return command_processor()
            else:
                return HttpResponseBadRequest()
        else:
            handler = getattr(super(), 'post', self.http_method_not_allowed)
            return handler(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if 'command' in self.request.GET:
            command_processor = getattr(self, 'send_{0}'.format(self.request.GET['command']), None)
            if command_processor is not None:
                return command_processor()
            else:
                return HttpResponseBadRequest()
        else:
            handler = getattr(super(), 'get', self.http_method_not_allowed)
            return handler(request, *args, **kwargs)

    def render_json(self, data, encoder=utils.JSONEncoder):
        return HttpResponse(
            json.dumps(data, indent=2, cls=encoder),
            content_type='application/json')


class GASMixin:
    base_role = 'admins'
    roles = set()
    base_template = 'gas/base.html'
    cancel_url = None
    continue_url = None
    header_title = ''
    title = ''
    help_text = ''
    success_message = _("Operation successful.")
    breadcrumbs = []
    actions = None

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        roles = set(self.roles)
        roles.add(self.base_role)
        access_denied = (
            not user.is_authenticated or (
                not user.is_superuser
                and user.user_roles.filter(role__in=roles).count() == 0
            )
        )
        if access_denied:
            return HttpResponseRedirect(reverse('gas:login') + '?next={}'.format(self.request.path))
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        if 'save_and_continue' in self.request.POST:
            response = HttpResponseRedirect(self.get_continue_url())
        messages.add_message(self.request, messages.SUCCESS, self.get_success_message())
        return response

    def get_success_message(self):
        return self.success_message

    def get_cancel_url(self):
        if self.cancel_url:
            # Forcing possible reverse_lazy evaluation
            url = str(self.cancel_url)
            return url
        else:
            return self.get_success_url()

    def get_continue_url(self):
        if self.continue_url:
            # Forcing possible reverse_lazy evaluation
            url = str(self.continue_url)
            return url
        else:
            raise ImproperlyConfigured("No URL to redirect to. Provide a continue_url.")

    def get_header_title(self):
        " Contents for the <title> tag. "
        return self.header_title or self.title

    def get_title(self):
        " Contents for page title. "
        return self.title

    def get_help_text(self):
        " Contents for page help. "
        return self.help_text

    def get_breadcrumbs(self):
        " Returns a list of (url, label) tuples for the breadcrumbs "
        return self.breadcrumbs

    def get_actions(self):
        return self.actions or []

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        css = gas_settings.MEDIA['css']
        js = gas_settings.MEDIA['js']
        if gas_settings.EXTRA_MEDIA:
            css = css + gas_settings.EXTRA_MEDIA.get('css', [])
            js = js + gas_settings.EXTRA_MEDIA.get('js', [])
        ctx.update({
            'base_template': self.base_template,
            'header_title': self.get_header_title(),
            'title': self.get_title(),
            'help_text': self.get_help_text(),
            'breadcrumbs': self.get_breadcrumbs(),
            'actions': self.get_actions(),
            'gas_title': gas_settings.TITLE,
            'logo_static_url': gas_settings.LOGO,
            'css': css,
            'js': js,
        })
        return ctx


class GASListView(GASMixin, ListView):
    """  ListView, permite indicar un formulario para filtrar contenido. """
    filter_form_class = None

    def get_filter_form(self):
        if self.filter_form_class is None:
            return None
        data = self.request.GET
        return self.filter_form_class(data=data)

    def filter_queryset(self, qs):
        self.filter_form = self.get_filter_form()
        if self.filter_form is not None and self.filter_form.is_valid():
            return self.filter_form.filter(qs)
        else:
            return qs

    def get_queryset(self):
        qs = super().get_queryset()
        return self.filter_queryset(qs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'filter_form': self.filter_form,
        })
        return ctx


class GASCreateView(GASMixin, CreateView):
    template_name = 'gas/base_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        is_popup = "_popup" in self.request.GET
        ctx.update({
            'is_popup': is_popup,
        })
        return ctx

    def form_valid(self, form):
        response = super().form_valid(form)
        if '_popup' in self.request.POST:
            return HttpResponse(
                '<!DOCTYPE html><html><head><title></title></head><body>'
                '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script></body></html>' %
                # escape() calls force_text.
                (escape(self.object.pk), escapejs(self.object)))
        else:
            return response


class GASUpdateView(GASMixin, UpdateView):
    """ Same as Django's UpdateView, defined only for completeness. """
    template_name = 'gas/base_form.html'


class GASDeleteView(GASMixin, DeleteView):
    template_name = "gas/delete_confirmation.html"
    confirmation_text = _("Are you sure you want to delete {object}?")
    deleted_text = _("{object} deleted.")
    show_deleted_objects = True

    def get_confirmation_text(self):
        return self.confirmation_text.format(object=self.object)

    def get_deleted_text(self):
        return self.deleted_text.format(object=self.object)

    def get_deleted_objects(self):
        using = router.db_for_write(self.model)
        collector = NestedObjects(using=using)

        def format_callback(obj):
            opts = obj._meta
            return '%s: %s' % (capfirst(opts.verbose_name), obj)

        collector.collect([self.object])
        model_count = {model._meta.verbose_name_plural: len(objs) for model, objs in collector.model_objs.items()}
        return collector.nested(format_callback), model_count

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if self.show_deleted_objects:
            deleted_objects, deleted_model_count = self.get_deleted_objects()
        else:
            deleted_objects = deleted_model_count = None

        ctx.update({
            'confirmation_text': self.get_confirmation_text(),
            'cancel_url': self.get_success_url(),
            'show_deleted_objects': self.show_deleted_objects,
            'deleted_objects': deleted_objects,
            'deleted_model_count': deleted_model_count,
        })
        return ctx

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.add_message(request, messages.SUCCESS, self.get_deleted_text())
        return response
