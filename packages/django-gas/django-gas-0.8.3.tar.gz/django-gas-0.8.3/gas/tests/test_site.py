from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.urls import reverse

from gas.sites import GASSite, site


class SiteTestCase(TestCase):
    def test_register_role(self):
        test_site = GASSite()

        # new role registered without error
        test_site.register_role('test', 'test role')

        # another new role registered without error
        test_site.register_role('test2', 'another test role')

        # repeated role raises error
        with self.assertRaises(ImproperlyConfigured):
            test_site.register_role('test', 'repeated test role')

    def test_register_urls(self):
        test_site = GASSite()

        # new prefix registered without error
        test_site.register_urls('test_prefix', 'gas.gas.urls')

        # another new prefix registered without error
        test_site.register_urls('test_prefix2', 'gas.gas.urls')

        # repeated prefix raises error
        with self.assertRaises(ImproperlyConfigured):
            test_site.register_urls('test_prefix', 'gas.gas.urls')

    def test_register_menu(self):
        test_site = GASSite()
        test_site.register_role('test_admins', 'test administrators')

        # Menu entry with non existent parent raises error
        with self.assertRaises(ImproperlyConfigured):
            test_site.register_menu(
                parent='nonexistent',
                name='test_roles',
                label="Roles",
                icon="",
                url="gas:role_list",
                roles=('test_admins',),
            )

        # new entry without parent without error
        test_site.register_menu(
            name='sample_app',
            label="Sample app",
            icon="",
            url=None,
            roles=('test_admins',),
        )

        # new entry with known parent without error
        test_site.register_menu(
            parent='sample_app',
            name='test_roles',
            label="Roles",
            icon="",
            url="gas:role_list",
            roles=('test_admins',),
        )
        # new entry with duplicated name raises error
        with self.assertRaises(ImproperlyConfigured):
            test_site.register_menu(
                name='sample_app',
                label="Sample app 2",
                icon="",
                url=None,
                roles=('test_admins',),
            )

        # new entry with no role
        test_site.register_menu(
            parent='sample_app',
            name='no_roles',
            label="No Roles",
            icon="",
            url="gas:role_list",
        )

    def test_menu_ordering(self):
        test_site = GASSite()
        admin_roles = set(('admins',))

        # With no explicit order, sort by label
        test_site.register_menu(name='c', label="c")
        test_site.register_menu(name='b', label="b")
        test_site.register_menu(name='a', label="a")
        entries = [
            entry.name
            for entry in sorted(test_site.get_root_menu(admin_roles))
        ]
        self.assertEqual(entries, ['a', 'b', 'c'])

        # Explicit order takes preference
        test_site.register_menu(name='z', label="z", order=1)
        entries = [
            entry.name
            for entry in sorted(test_site.get_root_menu(admin_roles))
        ]
        self.assertEqual(entries, ['z', 'a', 'b', 'c'])

        # Explicit order inside parent don't change the order
        test_site.register_menu(name='y', label="y", order=2, parent='a')
        entries = [
            entry.name
            for entry in sorted(test_site.get_root_menu(admin_roles))
        ]
        self.assertEqual(entries, ['z', 'a', 'b', 'c'])

        # With same explicit order, sort by label
        test_site.register_menu(name='x', label="x", order=1)
        entries = [
            entry.name
            for entry in sorted(test_site.get_root_menu(admin_roles))
        ]
        self.assertEqual(entries, ['x', 'z', 'a', 'b', 'c'])

    def test_menu_visibility(self):
        test_site = GASSite()
        admin_roles = set(('admins',))
        staff_roles = set(('staff',))

        test_site.register_menu(name='a', label='a', roles=admin_roles)
        test_site.register_menu(name='b', label='b', roles=staff_roles)

        # Admins gets all menu
        entries = [
            entry.name
            for entry in test_site.get_root_menu(admin_roles)
        ]
        self.assertEqual(entries, ['a', 'b'])

        # Staff gets filtered menu
        entries = [
            entry.name
            for entry in test_site.get_root_menu(staff_roles)
        ]
        self.assertEqual(entries, ['b'])


class SampleAppIntegrationTest(TestCase):
    def test_gas_autodiscover(self):
        # urls registered
        reverse('gas:index')

        # role registered
        self.assertIn(
            'admins',
            site._registry['roles'],
        )
