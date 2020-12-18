from django.conf.urls import url, include
from django_spaghetti.views import Plate

urlpatterns = [
    url(r'^$', Plate.as_view(
        plate_template_name="tests/home_plate.html"
    ), name='test_plate_override$'),
    url(r'^test/plate_settings$', Plate.as_view(
        settings={
            'apps': ['auth'],
            'exclude': {},
        }
    ), name='test_plate_settings'),
    url(r'^test/plate_show_m2m_field_detail$', Plate.as_view(
        override_settings={
            'show_m2m_field_detail': True
        }
    ), name='test_plate_show_m2m_field_detail'),
    url(r'^test/plate_override$', Plate.as_view(
        override_settings={
            'exclude': {
                'tests': ['policestation']
            },
        },
        meatball_template_name="tests/meatball.html"
    ), name='test_plate_override'),
    url(r'plate', include('django_spaghetti.urls', namespace="spaghetti")),
]
