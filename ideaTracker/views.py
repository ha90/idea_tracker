from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Idea

# Create your views here.
def index(request):
    idea_list = Idea.objects.all()
    template = loader.get_template('ideaTracker/index.html')
    context = {
        'idea_list': idea_list,
    }
    return HttpResponse(template.render(context, request));

def detail(request, idea_id):
    try:
        idea = Idea.objects.get(pk=idea_id)
    except Idea.DoesNotExist:
        raise Http404("Idea does not exist");
    return render(request, 'ideaTracker/detail.html', {'idea': idea})

