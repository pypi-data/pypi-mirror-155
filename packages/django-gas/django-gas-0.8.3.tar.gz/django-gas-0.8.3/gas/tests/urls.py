from django.urls import path, include
import gas.sites


urlpatterns = [
    path('control-panel/', include(gas.sites.site.urls)),
]
