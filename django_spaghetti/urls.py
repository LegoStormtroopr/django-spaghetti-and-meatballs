from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^plate/$', 'django_spaghetti.views.plate', name='plate'),
)
