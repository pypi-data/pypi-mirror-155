import datetime
import json

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from model_bakery import baker

from gas import utils


class UtilsTestCase(TestCase):
    def test_jsonencoder(self):
        users = baker.make('auth.User', _quantity=3)
        now = datetime.datetime.now()
        today = datetime.date.today()
        data = {
            'now': now,
            'today': today,
            'users': User.objects.all().values_list('pk', flat=True),
            'lazy_string': _('lazy'),
        }

        dumped_data = json.dumps(data, cls=utils.JSONEncoder)
        recovered_data = json.loads(dumped_data)

        self.assertEqual(
            recovered_data['now'],
            now.strftime('%Y-%m-%d %H:%M')
        )
        self.assertEqual(
            recovered_data['today'],
            today.strftime('%Y-%m-%d')
        )
        self.assertEqual(
            len(recovered_data['users']),
            3,
        )
        self.assertEqual(
            set(recovered_data['users']),
            set(user.pk for user in users),
        )
        self.assertEqual(
            recovered_data['lazy_string'], 'lazy',
        )
