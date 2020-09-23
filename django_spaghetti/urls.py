from django.urls import path
from django_spaghetti.views import plate

app_name = 'spaghetti'
urlpatterns = [
    path(r'', plate, name='plate'),
]
