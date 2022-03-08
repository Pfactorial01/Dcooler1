from . import views
from django.urls import path


urlpatterns = [
    path('',views.index,name="index"),
    path("login",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("demo_user",views.demo_view,name="demo_user"),
    path("Admin",views.Admin_view,name="Admin"),
    path("Admin1",views.Admin1_view,name="Admin1"),
    path("Admin2",views.Admin2_view,name="Admin2"),
    path("Dashboard",views.Dashboard,name="Dashboard"),
    path("Projects",views.Projects,name="Projects"),
    path("Roles",views.Roles,name="Roles"),
    path("new_project",views.new_project,name="new_project"),
    path("<int:projectid>",views.project_details,name="project_details"),
    path("edit_project<int:projectid>", views.edit_project,name="edit_project"),
    path("new_personnel",views.new_personnel,name="new_personnel"),
    path("edit_personnel<int:personnelid>",views.edit_personnel,name="edit_personnel"),
    path("issues",views.issues, name="issues"),
    path("new_issue",views.new_issue,name="new_issue"),
    path("issue<int:issueid>",views.issue_details,name="issue_details"),
    path("edit_issue<int:issueid>",views.edit_issue,name="edit_issue"),
    path("personnel<int:personnelid>",views.personnel_details,name="personnel_details")


]
