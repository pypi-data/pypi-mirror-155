from django.test import TestCase

from model_bakery import baker

from gas import models
from gas.sites import site


class UserRoleTestCase(TestCase):
    def test_str(self):
        user_role = baker.make('gas.UserRole')
        self.assertEqual(str(user_role), user_role.role)

    def test_description(self):
        user_role = baker.make('gas.UserRole')
        self.assertEqual(user_role.description, site.get_role_description(user_role.role))
