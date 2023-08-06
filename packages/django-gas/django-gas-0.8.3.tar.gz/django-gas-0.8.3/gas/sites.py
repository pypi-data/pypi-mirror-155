from django.urls import include, re_path
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import autodiscover_modules


class Entry:
    def __init__(self, name, label, icon=None, url=None, roles=None, parent=None, order=None):
        self.name = name
        self.label = label
        self.icon = icon
        self.url = url
        self.roles = roles
        self.children = dict()
        self.parent = parent
        self.order = order if order is not None else float("inf")

    def __lt__(self, other):
        if isinstance(other, Entry):
            return (self.parent, self.order, self.label) < (other.parent, other.order, other.label)
        return super().__lt__(other)


class GASSite(object):
    base_role = 'admins'

    def __init__(self):
        self._registry = {
            'menu': {},
            'urls': {},
            'roles': {},
        }
        self.autodiscover_done = False

    def register_role(self, name, description):
        if name in self._registry['roles']:
            raise ImproperlyConfigured("Role already registered")
        self._registry['roles'][name] = description

    def register_urls(self, prefix, urls):
        """
            Register urls with a prefix. Compared to normal urls, these are not
            exposed when gas is not active.
        """
        if prefix in self._registry['urls']:
            raise ImproperlyConfigured("Prefix {0} already in use".format(prefix))
        self._registry['urls'][prefix] = urls

    def register_menu(self, name, label, url=None, icon=None, roles=None, parent=None, order=None):
        if name in self._registry['menu']:
            raise ImproperlyConfigured("Menu entry '{0}' already registered.".format(name))

        if roles is None:
            roles = set()
        else:
            roles = set(roles)

        roles.add(self.base_role)

        entry = Entry(name, label, icon, url, roles, parent=parent, order=order)

        if parent:
            try:
                parent_entry = self._registry['menu'][parent]
            except KeyError:
                raise ImproperlyConfigured("Parent {} not registered.".format(parent))
            parent_entry.children[name] = entry

        self._registry['menu'][name] = entry

    @property
    def urls(self):
        return self.get_urls(), 'gas'

    @property
    def role_choices(self):
        return [
            (role, f"{role}: {description}")
            for role, description in self._registry['roles'].items()
        ]

    def get_role_description(self, role):
        return self._registry['roles'].get(role, '')

    def get_urls(self):
        urlpatterns = []
        for prefix, urls in self._registry['urls'].items():
            if prefix:
                urlpatterns.append(
                    re_path(r'^{0}/'.format(prefix), include(urls)),
                )
            else:
                urlpatterns.append(
                    re_path(r'', include(urls)),
                )
        return urlpatterns

    def get_root_menu(self, user_roles):
        entries = []
        for entry in self._registry['menu'].values():
            if entry.parent is not None:
                continue
            visible = user_roles.intersection(entry.roles)
            if not visible:
                continue
            entries.append(entry)
        return entries

    def autodiscover(self):
        if not self.autodiscover_done:
            autodiscover_modules('gas.config', register_to=site)
            self.autodiscover_done = True


site = GASSite()
