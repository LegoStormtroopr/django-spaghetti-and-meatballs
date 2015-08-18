from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from django.conf import settings
from django.db.models.fields import related
from django.template.loader import get_template
from django.template import Context

import json

graph_settings = getattr(settings, 'SPAGHETTI_SAUCE', {})
apps = graph_settings.get('apps',[])

def plate(request):
    excludes = ['%s__%s'%(app,model) for app,models in graph_settings.get('exclude',{}).items() for model in models ]
    models = ContentType.objects.filter(app_label__in=apps)
    nodes = []
    edges = []
    for model in models:
        model.doc  = model.model_class().__doc__
        _id = "%s__%s"%(model.app_label,model.model)
        if _id in excludes:
            continue
        label = "%s"%(model.model)
        fields = [f for f in model.model_class()._meta.fields if not str(f.name).endswith('_ptr')]
        many = [f for f in model.model_class()._meta.many_to_many]
        if graph_settings.get('show_fields',True):
            label += "\n%s\n"%("-"*len(model.model))
            label += "\n".join([str(f.name) for f in fields])
        edge_color = {'inherit':'from'}

        for f in fields:
            f.ftype = str(f.__class__).split('.')[-1][:-2]
            if type(f) == related.ForeignKey:
                _to = tuple(str(f.related_field).lower().split('.')[0:2])
                if _to[0] != model.app_label:
                    edge_color = {'inherit':'both'}
                edges.append(
                    {
                        'from':_id,
                        'to':"%s__%s"%_to,
                        'color':edge_color,
                        'arrows':{'to':{'scaleFactor':0.75}}
                    }
                )
        for f in many:
            #print dir(f)
            m = f.rel.to._meta
            #if m.app_label != model.app_label:
            edge_color = {'color':'gray'}
            edges.append(
                {
                    'from':_id,
                    'to':"%s__%s"%(m.app_label,m.model_name),
                    'color':edge_color,
                    'arrows':{'to':{'scaleFactor':0.5}, 'from':{'scaleFactor':0.5}},
                }
            )
        nodes.append(
            {
                'id':_id,
                'label':label,
                'shape':'box',
                'group':model.app_label,
                'title':get_template("django_spaghetti/meatball.html").render(
                    Context({'model':model,'fields':fields,})
                    )

            }
        )

    data = {
        'meatballs':json.dumps(nodes),
        'spaghetti':json.dumps(edges)
    }
    return render(request, 'django_spaghetti/plate.html', data)
