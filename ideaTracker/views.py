from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader

from .models import Idea

# Index page showing list of ideas added
def index(request):
    idea_list = Idea.objects.all()
    template = loader.get_template('ideaTracker/index.html')
    context = {
        'idea_list': idea_list,
    }
    return HttpResponse(template.render(context, request));

# View to add an idea
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

# Detailed view of an idea
def detail(request, idea_id):
    if request.method == 'POST':
        Idea.objects.filter(pk=idea_id).delete()
        return HttpResponseRedirect('/ideaTracker/')
    else:    
        try:
            idea = Idea.objects.get(pk=idea_id)
        except Idea.DoesNotExist:
            raise Http404("Idea does not exist");
        return render(request, 'ideaTracker/detail.html', {'idea': idea})

