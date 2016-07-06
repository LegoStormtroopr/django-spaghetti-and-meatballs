.. django-spaghetti-and-meatballs documentation master file, created by
   sphinx-quickstart on Sat Aug 22 00:56:36 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-spaghetti-and-meatballs's documentation!
==========================================================

Its a spicy meatball for serving up fresh hot entity-relationship diagrams straight from your django models.

Food puns aside, django-spaghetti-and-meatballs is a django app that extracts models
and documentation from a projects ``models.py`` to build rich, live, interactive
`entity-relationship diagrams <https://www.wikiwand.com/en/Entity%E2%80%93relationship_model>`_.

At the moment, it mines details from models:

 * docstrings, so documentation that the same documentation can be reused in the modeling
 * fields, including the fields datatype, help_text and cardinality
 * foreign and many-to-many relationships (at the moment only many-to-many relationships get special styling, but one-to-one is coming soon)

And it does this for all models in a project across any django apps you choose - plus you can specify models to exclude as well.

Why did you make this app?
--------------------------

There are a few really big use cases that I saw spaghetti-and-meatballs filling.

Firstly, for projects where generating user-facing diagrammatic representation of models helps with their understanding.
Being able to generate this from the code means that it is *never* out of sync with the actual design.

Secondly, being able to easily and graphically see the relationships between models shows where some models
are over- or under-connected. It also helps show where new connections can be useful, especially during development.

Lastly, it has been helpful during early stages of development as a prototyping and documentation tool.
Getting a simple and live view of all of the models and their documentation has been a godsend on a recent project when working
with non-developers. My preferred method of design and documentation is writing well documented code, which can be daunting for non-developers.
By using django models as an input to making the entity-relationship diagrams it means that diagrams of the structure of a project
and the code and documentation never get out of sync.
It also meant that I (and others) could easily spot gaps in documentation. While some code is self-documenting, hovering over
a model and still being confused about the existence of a field shows a definite need for explanation.

.. raw:: html

   <img src="https://cloud.githubusercontent.com/assets/2173174/9053053/a45e185c-3ab2-11e5-9ea0-89dafb7ac274.png"/>


Contents:

.. toctree::
   :maxdepth: 2

   ./installing.rst
   ./customising.rst
   ./contributing.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

