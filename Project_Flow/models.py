from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone

# Create your models here.

ROLES_CHOICES = (
    ("CEO","CEO"),
    ("Project Manager", "Project Manager"),
    ("Team Leader", "Team Leader"),
    ("Senior Technician", "Senior Technician"),
    ("Junior Technician", "Junior Technician")
)

class PersonnelManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class Personnel(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email address',max_length=254, unique=True)
    firstname = models.CharField(max_length=60)
    lastname = models.CharField(max_length=60)
    role = models.CharField(max_length=60, choices=ROLES_CHOICES,default="Junior Technician")
    projects = models.ManyToManyField("Project", related_name="personnels")

    USERNAME_FIELD = 'email'

    class Meta:
        app_label = 'Project_Flow'
    
    
    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.role})"
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    

    objects = PersonnelManager()

STATUS_CHOICES1 = (
    ("Inspection due", "Inspection due"),
    ("Finalised", "Finalised"),
    ("Procurement Due", "Procurement Due"),
    ("Mobilisation Due", "Mobilisation Due"),
    ("Construction Ongoing", "Construction Ongoing"),
    ("Completed", "Completed"),
    ("Handed Over", "Handed Over")
)

class ProjectManager(models.Manager):
    def get_by_natural_key(self, Project_Name):
        return self.get(Project_Name=Project_Name)

class Project(models.Model):
    Project_Name = models.CharField(max_length=200)
    Description = models.CharField(max_length=200)
    Deadline = models.DateField()
    personnel = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="projectsss")
    status =  models.CharField(max_length=60, choices=STATUS_CHOICES1,default="Inspection due")
    issues = models.ManyToManyField('Issue', blank=True, related_name="issuess")

    objects = ProjectManager()
    def natural_key(self):
        return (self.Project_Name)
    
    

    def __str__(self):
        return f"{self.Project_Name}"




class PersonnelManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    


        

    def create_staffuser(self, email, password=None):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email)
        user.staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        
        user.save(using=self._db)
        return user





















STATUS_CHOICES = (("resolved","resolved"),("unresolved","unresolved"))

class Issue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='project',default='')
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=200)
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=60, choices=STATUS_CHOICES,default="unresolved")

    def __str__(self):
        return f"{self.title}"

    