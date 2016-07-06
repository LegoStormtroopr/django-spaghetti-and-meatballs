from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from django.conf import settings
from django.db.models.fields import related
from django.template.loader import get_template
from django.template import Context
import json
from django.views.generic import View


class Plate(View):
    settings = None
    override_settings = {}
    template_name = 'django_spaghetti/plate.html'
    
    def get(self, request):
        return self.plate()

    def plate(self):
        request = self.request
        if self.settings is None:
            graph_settings = getattr(settings, 'SPAGHETTI_SAUCE', {})
            graph_settings.update(self.override_settings)
        else:
            graph_settings = self.settings
            
        apps = graph_settings.get('apps',[])
        

        excludes = ['%s__%s'%(app,model) for app,models in graph_settings.get('exclude',{}).items() for model in models ]
        models = ContentType.objects.filter(app_label__in=apps)
        nodes = []
        edges = []
        for model in models:
            if (model.model_class() == None):
                continue
            model.is_proxy = model.model_class()._meta.proxy
            if (model.is_proxy and not graph_settings.get('show_proxy',False)):
                continue
    
            model.doc  = model.model_class().__doc__
            _id = "%s__%s"%(model.app_label,model.model)
            if _id in excludes:
                continue

            label = self.get_node_label(model)

            fields = [f for f in model.model_class()._meta.fields]
            many = [f for f in model.model_class()._meta.many_to_many]
            if graph_settings.get('show_fields',True):
                label += "\n%s\n"%("-"*len(model.model))
                label += "\n".join([str(f.name) for f in fields])
            edge_color = {'inherit':'from'}
    
            for f in fields+many:
                if f.rel is not None:
                    m = f.rel.to._meta
                    to_id = "%s__%s"%(m.app_label,m.model_name)
                    print m
                    if not(_id == to_id and graph_settings.get('ignore_self_referential', False)):
                        if m.app_label != model.app_label:
                            edge_color = {'inherit':'both'}
                        
                        edge =  {'from':_id, 'to':to_id, 'color':edge_color }
        
                        if str(f.name).endswith('_ptr'):
                            # fields that end in _ptr are pointing to a parent object
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
            if model.is_proxy:
                proxy = model.model_class()._meta.proxy_for_model._meta
                model.proxy = proxy
                edge =  {   'to':_id,
                            'from':"%s__%s"%(proxy.app_label,proxy.model_name),
                            'color':edge_color,
                        }
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
        return render(request, self.template_name, data)

    def get_node_label(self,model):
        if model.is_proxy:
            label = "(P) %s"%(model.name.title())
        else:
            label = "%s"%(model.name.title())

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