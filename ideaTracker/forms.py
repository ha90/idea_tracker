from django import forms

class AddForm(forms.Form):
    title = forms.CharField(label='Title', max_length=40)
    description = forms.CharField(label='Description', max_length=140)
    PriorityChoices = ((1, 'Low'), (2, 'Medium'), (3, 'High'))
    priority = forms.ChoiceField(label='Priority', choices=PriorityChoices, initial=1)

# TODO can make this inherit from add form?
class EditForm(forms.Form):
    title = forms.CharField(label='Title', max_length=40)
    description = forms.CharField(label='Description', max_length=140)
