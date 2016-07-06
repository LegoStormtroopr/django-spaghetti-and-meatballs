Customising the output
======================

``Django-spaghetti-and-meatballs`` makes heavy use of the
`vis.js network library <http://visjs.org/network_examples.html>`_, so most
customisation is either based on django template modification and overrides
or changes to the vis.js settings. Knowing how to use both will make customisation
a breeze, but below are some simple recipes to get you started.

Serving up a new template
-------------------------

The default template is a frugal dish that serves spaghetti with no extras.
To serve the spaghetti in a fancier setting, just override the
``django_spaghetti/plate.html`` template in your projects ``templates`` directory.

You'll probably want your plate to look similar to that served by django_spaghetti,
`which can be viewed on github <https://github.com/LegoStormtroopr/django-spaghetti-and-meatballs/blob/master/django_spaghetti/templates/django_spaghetti/plate.html>`__ 

However, the important things when making a plate are:
 * make sure you import ``vis.js`` and ``vis.css`` *before* the script that creates the graph.
 * make your your script loads the ``meatballs`` (nodes) and ``spaghetti`` (edges) with the `safe django template filter <https://docs.djangoproject.com/en/1.8/ref/templates/builtins/#safe>`_
 
Changing how vis.js is loaded
-----------------------------

By default ``Django-spaghetti-and-meatballs`` loads ``vis.js`` from the
`Cloudflare CDN <http://cdnjs.com/libraries/vis>`_, but this might not be
appropriate for your project and may want to load it locally.

You can do this by following the above instructions and just changing the ``extra_scripts`` block.

Changing how vis.js lays out the graph
--------------------------------------

Dealing ``vis.js`` network customisation is beyond the scope of this project, but
`vis.js has comprehensive documentation of their network library available online <http://visjs.org/docs/network/>`_.
In the ``plate.html`` template you can make changes to the settings when you setup the graph.
By default ``django-spaghetti-and-meatballs`` uses a hierarchical layout, but any setup should work.
For example, to turn off hierarchical layout you can use the settings::

    "layout": {
        hierarchical: false,
    },

New flavours of meatballs
-------------------------

By default, ``django-spaghetti-and-meatballs`` shows a model with all its fields
and the documentation from the docstring in a hover over pop-up pane.
The layout for this box is included in the ``django_spaghetti/meatball.html``
template.
To change how models are shown on hover, just override the
``django_spaghetti/meatball.html`` template in your projects ``templates`` directory.

You'll probably want your meatball to taste similar to that served by django_spaghetti,
`which can be viewed on github <https://github.com/LegoStormtroopr/django-spaghetti-and-meatballs/blob/master/django_spaghetti/templates/django_spaghetti/meatball.html>`__ 

For example, to show just the models name, number of fields and its documentation your template would look like this::

    <div style="max-width:350px;white-space: normal;">
        <div style="border-bottom:1px solid black">
            Model: {{ model.model }}<br>
            # of fields: {{ fields|length }}
        </div>
        <tt style="white-space:pre-line">
            {{ model.doc }}
        </tt>
    </div>


Using class-based views
-----------------------

.. autoclass:: django_spaghetti.views.Plate
   :members: