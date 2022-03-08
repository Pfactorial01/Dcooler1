from django import forms
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.widgets import SelectDateWidget
from .models import Issue, Project,Personnel
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm



class NewPersonnelForm(UserCreationForm):

    class Meta:
        model = Personnel
        fields = ('email','firstname','lastname','role')

class NewProjectForm(ModelForm):
    personnel= forms.ModelMultipleChoiceField(
            queryset=Personnel.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )    
    class Meta:
        model = Project
        fields = ['Project_Name','Description','Deadline','personnel','status']
                
    staticmethod
    def __init__(self,*args,**kwargs):
        super(NewProjectForm, self).__init__(*args,**kwargs)
        self.fields['Deadline'].widget = SelectDateWidget()

        
        
       



        

class NewIssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['project','title','description','status']

    
        
