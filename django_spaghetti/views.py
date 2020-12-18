from copy import deepcopy

from django.apps import apps
from django.shortcuts import render

from django.conf import settings
from django.db.models.fields import related
from django.template.loader import get_template
import json
from django.views.generic import TemplateView


class Plate(TemplateView):
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

    def get_view_settings(self):
        if self.settings is None:
            graph_settings = deepcopy(getattr(settings, 'SPAGHETTI_SAUCE', {}))
            graph_settings.update(self.override_settings)
        else:
            graph_settings = self.settings
        return graph_settings

    def get_apps_list(self):
        return self.get_view_settings().get('apps', [])

    def get_excluded_models(self):
        return [
            "%s__%s" % (app, model)
            for app, models in self.get_view_settings().get('exclude', {}).items()
            for model in models
        ]

    def get_models(self):
        apps_list = self.get_apps_list()

        excludes = self.get_excluded_models()

        models = apps.get_models()
        _models = []
        for model in models:
            if (model is None):
                continue

            app_label = model._meta.app_label
            model_name = model._meta.model_name

            if app_label not in apps_list:
                continue

            model.is_proxy = model._meta.proxy
            if (model.is_proxy and not self.get_view_settings().get('show_proxy', False)):
                continue

            _id = "%s__%s" % (app_label, model_name)
            if _id in excludes:
                continue

            _models.append(model)

        return _models

    def get_group(self, model):
        return model._meta.app_label

    def get_colours(self):
        return ['red', 'blue', 'green', 'yellow', 'orange']

    def get_groups(self):
        colours = self.get_colours()
        groups = {}
        for app, colour in zip(sorted(self.get_apps_list()), colours):
            app_info = apps.get_app_config(app)
            groups.update({
                app: {
                    "color": {
                        'background': colour,
                        'border': 'gray'
                    },
                    "data": {
                        'name': str(app_info.verbose_name)
                    }
                }
            })
        return groups

    def include_link_to_field(self, model, field):
        return True

    def generate_edge_style(self, model, field):
        edge_style = {}
        if str(field.name).endswith('_ptr'):
            # fields that end in _ptr are pointing to a parent object
            edge_style.update({
                'arrows': {'to': {'scaleFactor': 0.75}},  # needed to draw from-to
                'font': {'align': 'middle'},
                'label': 'is a',
                'dashes': True
            })
        elif isinstance(field, related.ForeignKey):
            edge_style.update({
                'arrows': {'to': {'scaleFactor': 0.75}}
            })
        elif isinstance(field, related.OneToOneField):
            edge_style.update({
                'font': {'align': 'middle'},
                'label': '|'
            })
        elif isinstance(field, related.ManyToManyField):
            edge_style.update({
                'color': {'color': 'gray'},
                'arrows': {'to': {'scaleFactor': 1}, 'from': {'scaleFactor': 1}},
            })
        return edge_style

    def get_fields_for_model(self, model):
        fields = [f for f in model._meta.fields]
        many = [f for f in model._meta.many_to_many]
        return fields + many

    def get_link_fields_for_model(self, model):
        return [
            f
            for f in self.get_fields_for_model(model)
            if f.remote_field is not None and self.include_link_to_field(model, f)
        ]

    def get_id_for_model(self, model):
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        return "%s__%s" % (app_label, model_name)

    def plate(self):
        """
        Serves up a delicious plate with your models
        """
        request = self.request
        graph_settings = self.get_view_settings()

        excludes = self.get_excluded_models()

        nodes = []
        edges = []
        for model in self.get_models():
            app_label = model._meta.app_label
            model_name = model._meta.model_name
            model.doc = model.__doc__
            _id = self.get_id_for_model(model)

            label = self.get_node_label(model)

            node_fields = self.get_fields_for_model(model)

            if graph_settings.get('show_fields', True):
                label += "\n%s\n" % ("-" * len(model_name))
                label += "\n".join([str(f.name) for f in node_fields])
            edge_color = {'inherit': 'from'}

            for f in self.get_link_fields_for_model(model):
                m = f.remote_field.model
                to_id = self.get_id_for_model(f.remote_field.model)
                if to_id in excludes:
                    pass
                elif _id == to_id and graph_settings.get('ignore_self_referential', False):
                    pass
                else:
                    if m._meta.app_label != app_label:
                        edge_color = {'inherit': 'both'}

                    edge = {'from': _id, 'to': to_id, 'color': edge_color}

                    edge.update(self.generate_edge_style(model, f))
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

            nodes.append(
                {
                    'id': _id,
                    'label': label,
                    'shape': 'box',
                    'group': self.get_group(model),
                    'title': get_template(self.meatball_template_name).render(
                        {'model': model, 'model_meta': model._meta, 'fields': node_fields}
                    ),
                    'data': self.get_extra_node_data(model)
                }
            )
        context = self.get_context_data()
        context.update({
            'meatballs': json.dumps(nodes),
            'spaghetti': json.dumps(edges),
            'groups': json.dumps(self.get_groups()),
        })
        return render(request, self.plate_template_name, context)

    def get_extra_node_data(self, model):
        return {}

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
