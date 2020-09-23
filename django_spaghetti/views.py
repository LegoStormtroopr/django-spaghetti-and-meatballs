from copy import deepcopy

from django.shortcuts import render

from django.conf import settings
from django.db.models.fields import related
from django.template.loader import get_template
import json
from django.views.generic import View


class Plate(View):
    """
    This class-based-view serves up spaghetti and meatballs.

    Override the following class properties when calling `as_view`:

    * `settings` - sets a view specific to use instead of the `SPAGHETTI_SAUCE` django settings
    * `override_settings` - overrides specified settings from `SPAGHETTI_SAUCE` django settings
    * `plate_template_name` - overrides the template name for the whole view
    * `meatball_template_name` - overrides the template used to render nodes

    For example the below URL pattern would specify a path to a view that displayed
    models from the `auth` app with the given templates::

        url(r'^user_graph/$',
            Plate.as_view(
                settings = {
                    'apps': ['auth'],
                }
                meatball_template_name = "my_app/user_node.html",
                plate_template_name = "my_app/auth_details.html"
        )
    """
    settings = None
    override_settings = {}
    plate_template_name = 'django_spaghetti/plate.html'
    meatball_template_name = "django_spaghetti/meatball.html"

    def get(self, request):
        return self.plate()

    def plate(self):
        """
        Serves up a delicious plate with your models
        """
        request = self.request
        if self.settings is None:
            graph_settings = deepcopy(getattr(settings, 'SPAGHETTI_SAUCE', {}))
            graph_settings.update(self.override_settings)
        else:
            graph_settings = self.settings

        apps = graph_settings.get('apps', [])

        excludes = [
            "%s__%s" % (app, model)
            for app, models in graph_settings.get('exclude', {}).items()
            for model in models
        ]
        from django.apps import apps

        models = apps.get_models()
        nodes = []
        edges = []
        for model in models:
            if (model is None):
                continue
            model.is_proxy = model._meta.proxy
            if (model.is_proxy and not graph_settings.get('show_proxy', False)):
                continue

            model.doc = model.__doc__

            app_label = model._meta.app_label
            model_name = model._meta.model_name
            _id = "%s__%s" % (app_label, model_name)
            if _id in excludes:
                continue

            label = self.get_node_label(model)

            fields = [f for f in model._meta.fields]
            many = [f for f in model._meta.many_to_many]
            if graph_settings.get('show_fields', True):
                label += "\n%s\n" % ("-" * len(model.model_name))
                label += "\n".join([str(f.name) for f in fields])
            edge_color = {'inherit': 'from'}

            for f in fields + many:
                if f.remote_field is not None:
                    m = f.remote_field.model._meta
                    to_id = "%s__%s" % (m.app_label, m.model_name)
                    if to_id in excludes:
                        pass
                    elif _id == to_id and graph_settings.get('ignore_self_referential', False):
                        pass
                    else:
                        if m.app_label != app_label:
                            edge_color = {'inherit': 'both'}

                        edge = {'from': _id, 'to': to_id, 'color': edge_color}

                        if str(f.name).endswith('_ptr'):
                            # fields that end in _ptr are pointing to a parent object
                            edge.update({
                                'arrows': {'to': {'scaleFactor': 0.75}},  # needed to draw from-to
                                'font': {'align': 'middle'},
                                'label': 'is a',
                                'dashes': True
                            })
                        elif type(f) == related.ForeignKey:
                            edge.update({
                                'arrows': {'to': {'scaleFactor': 0.75}}
                            })
                        elif type(f) == related.OneToOneField:
                            edge.update({
                                'font': {'align': 'middle'},
                                'label': '|'
                            })
                        elif type(f) == related.ManyToManyField:
                            edge.update({
                                'color': {'color': 'gray'},
                                'arrows': {'to': {'scaleFactor': 1}, 'from': {'scaleFactor': 1}},
                            })

                        edges.append(edge)
            if model.is_proxy:
                proxy = model._meta.proxy_for_model._meta
                model.proxy = proxy
                edge = {
                    'to': _id,
                    'from': "%s__%s" % (proxy.app_label, proxy.model_name),
                    'color': edge_color,
                }
                edges.append(edge)

            all_node_fields = fields
            if graph_settings.get('show_m2m_field_detail', False):
                all_node_fields = fields + many
            nodes.append(
                {
                    'id': _id,
                    'label': label,
                    'shape': 'box',
                    'group': app_label,
                    'title': get_template(self.meatball_template_name).render(
                        {'model': model, 'fields': all_node_fields}
                        )
                }
            )
        data = {
            'meatballs': json.dumps(nodes),
            'spaghetti': json.dumps(edges)
        }
        return render(request, self.plate_template_name, data)

    def get_node_label(self, model):
        """
        Defines how labels are constructed from models.
        Default - uses verbose name, lines breaks where sensible
        """
        if model.is_proxy:
            label = "(P) %s" % (model._meta.verbose_name.title())
        else:
            label = "%s" % (model._meta.verbose_name.title())

        line = ""
        new_label = []
        for w in label.split(" "):
            if len(line + w) > 15:
                new_label.append(line)
                line = w
            else:
                line += " "
                line += w
        new_label.append(line)

        return "\n".join(new_label)

plate = Plate.as_view()
