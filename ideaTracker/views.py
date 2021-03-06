from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader

from .models import Idea
from .forms import AddForm, EditForm
from .utils  import IdeaState, getStatesInDict
from datetime import datetime

# Index page showing list of ideas added
def index(request):
    # get all ideas ordered by priority from db
    idea_list = Idea.objects.all().order_by('priority')
    # get the template used to display the items
    template = loader.get_template('ideaTracker/index.html')
    # context passed to the template
    context = {
        'idea_list': idea_list,
    }
    return HttpResponse(template.render(context, request));

# View to add an idea
def add(request):
    # if we came here by post request, user has filled the add form
    if request.method == 'POST':
        # get the form from request 
        form = AddForm(request.POST)
        # check if form is valid
        if form.is_valid():
            # get form data 
            title       = form.cleaned_data['title']
            description = form.cleaned_data['description']
            priority    = form.cleaned_data['priority']
            # add the idea in the db
            Idea.objects.create(title = title,
                                description = description,
                                state = IdeaState.NEW.value,
                                priority = priority)
            # redirect user to idea list page  
            return HttpResponseRedirect('/ideaTracker/')
        """
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
        """        
    else:
        # we came here by get request, show the user the add form
        form = AddForm()
        return render(request, 'ideaTracker/add.html', {'form' : form})

# View to edit an idea        
def edit(request, idea_id):
    # if we came here via post request  
    if request.method == 'POST':
        if 'save' in request.POST:
            # get the form from request 
            form = EditForm(request.POST)
            # check if form is valid
            if form.is_valid():
                # get form data 
                title       = form.cleaned_data['title']
                description = form.cleaned_data['description']

            #TODO Put safety or move to common function for form validation
            state   = request.POST['state']

            # update idea in db
            Idea.objects.filter(pk=idea_id).update(title = title,
                                                   description = description,
                                                   state=state,
                                                   modified_date=datetime.now())
            return HttpResponseRedirect('/ideaTracker/')
        elif 'cancel' in request.POST:
            return HttpResponseRedirect('/ideaTracker/')
        else:
            return HttpResponse("Somethings wrong")
    else:
        # get idea from db
        idea = Idea.objects.get(pk=idea_id) 
        # get idea states. TODO any other way for this?
        ideaStates = getStatesInDict()
        # create form data
        formData = {'title' : idea.title, 'description' : idea.description}
        # create form
        form = EditForm(formData)
        return render(request, 'ideaTracker/edit.html', {'form' : form, 'idea': idea, 'ideaStates': ideaStates})

# Detailed view of an idea
def detail(request, idea_id):
    if request.method == 'POST':
        if 'delete' in request.POST:
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
