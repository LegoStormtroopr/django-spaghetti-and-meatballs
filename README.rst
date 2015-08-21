django-spaghetti-and-meatballs
==============================

Its a spicy meatball for serving up fresh hot entity-relationship diagrams straight from your django models.


Adding spaghetti to you project
-------------------------------

At this stage, you need to clone the repository and make sure the ``django_spaghetti``
directory is somewhere your project can import it.

Configure your sauce
++++++++++++++++++++

Insrall some spaghetti::

  pip install django-spaghetti-and-meatballs

Add ``"django_spaghetti"`` to your ``INSTALLED_APPS`` setting like this::

  INSTALLED_APPS = [
      ...
      'django_spaghetti',
  ]

``django-spaghetti-and-meatballs`` takes a few options set in the ``SPAGHETTI_SAUCE``
variable from your projects ``settings.py`` file that make it `extra spicy`::

  SPAGHETTI_SAUCE = {
    'apps':['auth','polls'],
    'show_fields':False,
    'exclude':{'auth':['user']}
  }

In the above dictionary, the settings mean:

* ``apps`` is a list of apps you want to show in the graph. If its `not` in here it `won't be seen`.
* ``show_fields`` is a boolean that states if the field names should be shown in the graph or just in the however over. For small graphs, you can set this to `True` to show fields as well, but as you get more models it gets messier.
* ``exclude`` is a dictionary where each key is an ``app_label`` and the items for that key are model names to hide in the graph. 

If its not working as expected make sure your app labels and model names are all **lower case**.


Serve your plate in your urls file
++++++++++++++++++++++++++++++++++

Once you've configured your sauce, make sure you serve up a plate of spaghetti in your ``urls.py`` like so::

    urlpatterns += patterns('',
      url(r'^plate/', include('django_spaghetti.urls')),
    )

A sample platter
----------------

Below is an example image showing the connections between models from the 
`django-reversion <https://github.com/etianen/django-reversion>`_ and 
`django-notifications <https://github.com/django-notifications/django-notifications>`_ 
apps and Django's built-in ``auth`` models.

Colored edges illustrate foreign key relations, with arrows pointing from the defining 
model to the related model, while gray edges illustrate many-to-many relations. 
Different colors signify the different Django apps, and when relations link between 
apps the edges are colored with a gradient.

Hovering over a model, gives a pop-up that lists the following information:

* model name
* app label
* The models docstring
* A list of every field, with its field type and its help text (if defined). Unique fields have their name underlined.

This was build with the sauce::

  SPAGHETTI_SAUCE = {
    'apps':['auth','notifications','reversion'],
    'show_fields':False,
    }

A complex live-demo
-------------------

To see a complex example, where ``django-spaghetti-and-meatballs`` really shines,
checkout the live version built for the `Aristotle Metadata Registry <http://aristotle.pythonanywhere.com/plate/>`_
