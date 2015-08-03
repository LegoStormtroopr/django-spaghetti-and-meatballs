from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from django.conf import settings
from django.core import exceptions
from django.template.loader import get_template
from django.template import Context

from django.db.models.fields import related
import json

graph_settings = getattr(settings, 'GRAPH_MODELS', {})
apps = graph_settings.get('apps',[])

def plate(request):

    models = ContentType.objects.filter(app_label__in=apps)
    nodes = []
    edges = []
    for model in models:
        _id = "%s__%s"%(model.app_label,model.model)
        label = "%s.%s\n%s\n"%(model.app_label,model.model,"-"*len(model.model))
        label += "\n".join([str(f.name) for f in model.model_class()._meta.fields if not str(f.name).endswith('_ptr')])
        for f in model.model_class()._meta.fields:
            if type(f) == related.ForeignKey:
                #print dir(f)
                _to = tuple(str(f.related_field).lower().split('.')[0:2])
                #print f, f.related_field
                edges.append({'from':_id,'to':"%s__%s"%_to})
        nodes.append(
            {
                'id':_id,
                'label':label,
                'shape':'box',
                #'group':model.app_label
            }
        ) #.model_class()

    data = {
        'nodes':json.dumps(nodes),
        'edges':json.dumps(edges)
    }
    return render(request, 'django_spaghetti/plate.html', data)
