django-spaghetti-and-meatballs
------------------------------

An example image showing the connections between models from the `django-reversion <https://github.com/etianen/django-reversion>`_ and `django-notifications <https://github.com/django-notifications/django-notifications>`_ apps and Django's built-in ``auth`` models.

Colored edges illustrate foreign key relations, with arrows pointing from the defining model to the related model, while gray edges illustrate many-to-many relations. Different colors signify the different Django apps, and when relations link between apps the edges are colored with a gradient.

.. image:: https://cloud.githubusercontent.com/assets/2173174/9053053/a45e185c-3ab2-11e5-9ea0-89dafb7ac274.png

Hovering over a model, gives a pop-up that lists the following information:

* model name
* app label
* The models docstring
* A list of every field, with its field type and its help text (if defined). Unique fields have their name underlined.
