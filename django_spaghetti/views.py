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
        if (model.model_class() == None):
            continue

        model.doc  = model.model_class().__doc__
        _id = "%s__%s"%(model.app_label,model.model)
        if _id in excludes:
            continue
        label = "%s"%(model.model)
        fields = [f for f in model.model_class()._meta.fields]
        many = [f for f in model.model_class()._meta.many_to_many]
        if graph_settings.get('show_fields',True):
            label += "\n%s\n"%("-"*len(model.model))
            label += "\n".join([str(f.name) for f in fields])
        edge_color = {'inherit':'from'}

        for f in fields+many:
            if f.rel is not None:
                m = f.rel.to._meta
                if m.app_label != model.app_label:
                    edge_color = {'inherit':'both'}
                edge =  {   'from':_id,
                            'to':"%s__%s"%(m.app_label,m.model_name),
                            'color':edge_color,
                        }

                if str(f.name).endswith('_ptr'):
                    #fields that end in _ptr are pointing to a parent object
                    edge.update({
                    'arrows':{'to':{'scaleFactor':0.75}}, #needed to draw from-to
                    'font': {'align': 'middle'},
                    'label':'is a',
                    'dashes':True
                        })
                elif type(f) == related.ForeignKey:
                    edge.update({
                            'arrows':{'to':{'scaleFactor':0.75}}
                        })
                elif type(f) == related.OneToOneField:
                    edge.update({
                            'font': {'align': 'middle'},
                            'label':'|'
                        })
                elif type(f) == related.ManyToManyField:
                    edge.update({
                            'color':{'color':'gray'},
                            'arrows':{'to':{'scaleFactor':1}, 'from':{'scaleFactor':1}},
                        })

                edges.append(edge)

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
