from dataclasses import fields
from multiprocessing import context
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate
from json import dumps
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.core import serializers
from datetime import timedelta

from Project_Flow.models import Personnel, Project, Issue
from .forms import NewProjectForm, NewPersonnelForm, NewIssueForm

# Create your views here.




def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponseRedirect(reverse('Admin'))


def login_view(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('Admin'))
            
        else:
            return render(request,"Project_Flow/login.html",{
                "message": "Incorrect username or password!"
            })
    return render(request,"Project_Flow/login.html")

def logout_view(request):
    logout(request)
    return render(request,"Project_Flow/login.html",{
                "message": "Logged Out"
    })

def demo_view(request):
    return render(request,"Project_Flow/demo_user.html")

def Admin_view(request):
    result = Project.objects.all().order_by('Deadline')[:5]
    dataJSON = serializers.serialize("json", result)


    result1 = Issue.objects.all().order_by('-date_created')[:5]
    dataJSON1 = serializers.serialize("json", result1, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    context = {'result':dataJSON, 'result1':dataJSON1} 

    
    

    return render(request,"Project_Flow/Admin.html", context
    )

def Admin1_view(request):
    pass

def Admin2_view(request):
    pass

def Dashboard(request):
    pass

def Projects(request):
    
    result = Project.objects.all()
    
    dataJSON = serializers.serialize("json", result)
    context = {'result': dataJSON}

    return render(request,"Project_Flow/projectss.html", context)

def Roles(request):

    result = Personnel.objects.all()
    
    dataJSON = serializers.serialize("json", result)
    context = {'result': dataJSON}

    return render(request,"Project_Flow/role.html", context)

    
def new_project(request):
    form = NewProjectForm()     
    
    if request.method == 'POST':        
        form = NewProjectForm(request.POST)                                  
        
        if form.is_valid():    
            form.save()
            return HttpResponseRedirect(reverse("Projects"))

    context = {'form':form}
    return render(request, 'Project_Flow/new_projects.html', context)
    
def project_details(request,projectid):
    project = Project.objects.get(pk=projectid)
    return render(request, "Project_Flow/project_detail.html",{
        "project":project, "personnels":project.personnel.all()
        
    })

def edit_project(request,projectid):
    project = Project.objects.get(pk=projectid)
 
    form = NewProjectForm(instance=project)
    if request.method == 'POST':
        form = NewProjectForm(request.POST, instance=project)
        personnel = Personnel.objects.get(pk=int(request.POST["personnel"]))
        personnel.projects.add(project)
        if form.is_valid():
        
           form.save()
           return HttpResponseRedirect(reverse("project_details",args=(projectid,)))

    context = {"project":project,'form':form,"personnels":project.personnels.all(),
        "non_personnels":Personnel.objects.exclude(projects=project)
    }
    return render(request, 'Project_Flow/edit_projects.html', context)

def new_personnel(request):
    form = NewPersonnelForm()     
    
    if request.method == 'POST':        
        form = NewPersonnelForm(request.POST)                                  
        
        if form.is_valid():    
            form.save()
            return HttpResponseRedirect(reverse("Roles"))

    context = {'form':form}
    return render(request, 'Project_Flow/new_personnels.html', context)

def edit_personnel(request,personnelid):
    personnel = Personnel.objects.get(pk=personnelid)
 
    form = NewPersonnelForm(instance=personnel)
    if request.method == 'POST':
        form = NewPersonnelForm(request.POST, instance=personnel)
               
        if form.is_valid():        
           form.save()
           return HttpResponseRedirect(reverse("personnel_details",args=(personnelid,)))

    context = {"personnel":personnel,'form':form}
    return render(request, 'Project_Flow/edit_personnel.html', context)

def issues(request):
    result = Issue.objects.all()
    
    dataJSON = serializers.serialize("json", result, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    context = {'result': dataJSON}

    return render(request,"Project_Flow/issue.html", context)

def new_issue(request):
    form = NewIssueForm()     
    
    if request.method == 'POST':        
        form = NewIssueForm(request.POST)                                  
        
        if form.is_valid():  
            x = form.save(commit=False)
            x.submitter = request.user  
            form.save()            
            return HttpResponseRedirect(reverse("issues"))

    context = {'form':form}
    return render(request, 'Project_Flow/new_issues.html', context)
    
def issue_details(request,issueid):
    issue = Issue.objects.get(pk=issueid)
    context = {"issue":issue}
    return render(request, "Project_Flow/issue_detail.html",context)

def edit_issue(request, issueid):
    issue = Issue.objects.get(pk=issueid)
 
    form = NewIssueForm(instance=issue)
    if request.method == 'POST':
        form = NewIssueForm(request.POST, instance=issue)
               
        if form.is_valid():        
           form.save()
           return HttpResponseRedirect(reverse("issue_details",args=(issueid,)))

    context = {"issue":issue,'form':form}
    return render(request, 'Project_Flow/edit_issues.html', context)
    

def personnel_details(request,personnelid):    
    personnel = Personnel.objects.get(pk=personnelid)
    context = {"personnel":personnel, "projects":personnel.projects.all()} 
    
    return render(request, "Project_Flow/personnel_detail.html", context)

