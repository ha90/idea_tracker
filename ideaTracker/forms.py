from django import forms

class AddForm(forms.form):
    title = forms.CharField(label='Title', max_length=40)
    description = forms.CharField(label='Title', max_length=140)
