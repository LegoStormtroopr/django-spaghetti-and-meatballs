from django.conf.urls import url
from django.contrib import admin
from django_spaghetti.views import plate, Plate

urlpatterns = [
    url(r'^/', include('django_spaghetti.urls',namespace="spaghetti")),
    url(r'^test/plate_settings$', Plate.as_view(
        settings={
            'apps': ['auth'],
            'exclude': {},
        }
    ), name='test_plate_settings'),
    url(r'^test/plate_override$', Plate.as_view(
        override_settings={
            'exclude': {
                'tests': ['policestation']
            },
        },
        meatball_template_name="tests/meatball.html"
    ), name='test_plate_override$'),
]
