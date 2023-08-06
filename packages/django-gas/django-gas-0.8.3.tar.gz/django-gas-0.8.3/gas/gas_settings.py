from django.conf import settings


TITLE = getattr(settings, 'GAS_TITLE', 'GAS')
LOGO = getattr(settings, 'GAS_LOGO', 'gas/css/img/logo.svg')

MEDIA = getattr(settings, 'GAS_MEDIA', {
    'css': [
        'vendor/font-awesome/css/all.css',
        'vendor/select2/css/select2.css',
        'gas/css/gas.css',
    ],
    'js': [
        'vendor/jquery/dist/jquery.min.js',
        'vendor/jquery.formset.js',
        'vendor/select2/js/select2.full.min.js',
        'gas/js/add_popups.js',
        'gas/js/gas.js',
    ],
})

EXTRA_MEDIA = getattr(settings, 'GAS_EXTRA_MEDIA', None)
