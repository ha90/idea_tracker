from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader

from .models import Idea
from .utils  import IdeaState, getStatesInDict
from datetime import datetime

# Index page showing list of ideas added
def index(request):
    idea_list = Idea.objects.all().order_by('priority')
    template = loader.get_template('ideaTracker/index.html')
    context = {
        'idea_list': idea_list,
    }
    return HttpResponse(template.render(context, request));

# View to add an idea
def add(request):
    if request.method == 'POST':
        try:
            title    = request.POST['title']
            desc     = request.POST['desc']
            priority = request.POST['priority']
        except (KeyError):
            return HttpResponse("Please fill all data")
        else:
            #TODO make a function in utils to validated input and add
            Idea.objects.create(title = title, description = desc, state=IdeaState.NEW.value, priority = priority)
            return HttpResponseRedirect('/ideaTracker/')
    else:
        return render(request, 'ideaTracker/add.html', {})

# View to edit an idea        
def edit(request):
    print ("View: EDIT")
    if request.method == 'POST':
        if 'save' in request.POST:
            #TODO Put safety or move to common function for form validation
            title   = request.POST['title']
            desc    = request.POST['desc']
            state   = request.POST['state']
            idea_id = request.POST['idea_id']
            Idea.objects.filter(pk=idea_id).update(title = title,
                                                   description = desc,
                                                   state=state,
                                                   modified_date=datetime.now())
            return HttpResponseRedirect('/ideaTracker/')
        elif 'cancel' in request.POST:
            return HttpResponseRedirect('/ideaTracker/')
        elif 'idea_id' in request.POST:
            #TODO seems redundant (present here and in detail)
            idea_id = request.POST['idea_id']
            #TODO put safety check for idea not present
            idea = Idea.objects.get(pk=idea_id)
            return render(request, 'ideaTracker/edit.html', {'idea': idea})
        else:
            return HttpResponse("Somethings wrong")
    else:
        return HttpResponseRedirect('/ideaTracker/')

# Detailed view of an idea
def detail(request, idea_id):
    if request.method == 'POST':
        if 'edit' in request.POST:
            idea_id = request.POST['idea_id']
            idea = Idea.objects.get(pk=idea_id)
            ideaStates = getStatesInDict()
            return render(request, 'ideaTracker/edit.html', {'idea': idea, 'ideaStates': ideaStates})
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
