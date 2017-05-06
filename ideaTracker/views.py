from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader

from .models import Idea
from .utils  import IdeaState

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
            #TODO make a function in utils to validated input and add
            Idea.objects.create(title = title, description = desc, state=IdeaState.NEW)
            return HttpResponseRedirect('/ideaTracker/')
    else:
        return render(request, 'ideaTracker/add.html', {})

# View to edit an idea        
def edit(request):
    if request.method == 'POST':
        try:
            idea_id = request.POST['idea_id']
        except (KeyError):
            return HttpResponse("Somethings wrong")
        else:
            #TODO
            return HttpResponse("Not yet available")
    else:
        return HttpResponseRedirect('/ideaTracker/')

# Detailed view of an idea
def detail(request, idea_id):
    if request.method == 'POST':
        if 'edit' in request.POST:
            return render(request, 'ideaTracker/edit.html', {'idea_id': idea_id})
        elif 'delete' in request.POST:
                Idea.objects.filter(pk=idea_id).delete()
                return HttpResponseRedirect('/ideaTracker/')
        else:
            return HttpResponse("Something's wrong")
    else:    
        try:
            idea = Idea.objects.get(pk=idea_id)
        except Idea.DoesNotExist:
            raise Http404("Idea does not exist");
        return render(request, 'ideaTracker/detail.html', {'idea': idea, 'state': IdeaState(idea.state).name})
