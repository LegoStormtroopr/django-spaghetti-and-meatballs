from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from django.conf import settings
from django.db.models.fields import related
from django.template.loader import get_template
from django.template import Context

import json

graph_settings = getattr(settings, 'GRAPH_MODELS', {})
apps = graph_settings.get('apps',[])

def plate(request):

    models = ContentType.objects.filter(app_label__in=apps)
    nodes = []
    edges = []
    for model in models:
        model.doc  = model.model_class().__doc__
        _id = "%s__%s"%(model.app_label,model.model)
        label = "%s"%(model.model)
        fields = [f for f in model.model_class()._meta.fields if not str(f.name).endswith('_ptr')]
        if graph_settings.get('show_fields',True):
            label += "\n%s\n"%("-"*len(model.model))
            label += "\n".join([str(f.name) for f in fields])
        for f in fields:
            f.ftype = str(f.__class__).split('.')[-1][:-2]
            if type(f) == related.ForeignKey:
                #print dir(f)
                _to = tuple(str(f.related_field).lower().split('.')[0:2])
                #print f, f.related_field
                edges.append(
                    {
                        'from':_id,
                        'to':"%s__%s"%_to,
                        'arrows':{'to':{'scaleFactor':0.5}}
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
