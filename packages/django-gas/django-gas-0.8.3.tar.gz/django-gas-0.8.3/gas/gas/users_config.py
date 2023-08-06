from django.utils.translation import gettext_lazy as _

from gas.sites import site


site.register_urls('users', 'gas.gas.users.urls')
site.register_menu(
    name='users',
    label=_("Users"),
    icon="",
    url="gas:user_list",
    roles=('admins',),
)
