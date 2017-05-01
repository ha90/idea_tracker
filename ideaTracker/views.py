from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
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

def add(request):
    if request.method == 'POST':
        try:
            title = request.POST['title']
            desc  = request.POST['desc']
        except (KeyError):
            return HttpResponse("Please fill all data")
        else:
            Idea.objects.create(title = title, description = desc)
            return HttpResponseRedirect('/ideaTracker/')
    else:
        return render(request, 'ideaTracker/add.html', {})

def detail(request, idea_id):
    try:
        idea = Idea.objects.get(pk=idea_id)
    except Idea.DoesNotExist:
        raise Http404("Idea does not exist");
    return render(request, 'ideaTracker/detail.html', {'idea': idea})

