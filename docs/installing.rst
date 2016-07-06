Installing and configuring
==========================

Installing spaghetti
--------------------

1. Install some spaghetti::

    pip install django-spaghetti-and-meatballs

2. Add ``"django_spaghetti"`` to your ``INSTALLED_APPS`` setting like this::

    INSTALLED_APPS = [
      ...
      'django_spaghetti',
    ]

3. Add a plate of spaghetti in your ``urls.py`` like so::

    urlpatterns += patterns('',
      url(r'^plate/', include('django_spaghetti.urls')),
    )

4. Or use the class-based view if you want more flexibility::

    urlpatterns += patterns('',
      url(r'^plate/$',
        Plate.as_view(
          override_settings = {
              'apps':['auth','polls'],
            }
        ),
        name='plate'
      ),
    )


Configuring meatballs
---------------------

``django-spaghetti-and-meatballs`` takes a few options set in the ``SPAGHETTI_SAUCE``
variable from your projects ``settings.py`` file that make it `extra spicy`::

  SPAGHETTI_SAUCE = {
    'apps':['auth','polls'],
    'show_fields':False,
    'exclude':{'auth':['user']},
    'show_proxy':True,
  }

In the above dictionary, the following settings are used:

* ``apps`` is a list of apps you want to show in the graph. If its `not` in here it `won't be seen`.
* ``show_fields`` is a boolean that states if the field names should be shown in the graph or just in the however over. For small graphs, you can set this to `True` to show fields as well, but as you get more models it gets messier.
* ``exclude`` is a dictionary where each key is an ``app_label`` and the items for that key are model names to hide in the graph. 
* ``show_proxy`` is boolean, if truthy proxy models will be shown and linked to their main model, otherwise they will be hidden. By default this is false.

If its not working as expected make sure your app labels and model names are all **lower case**.

