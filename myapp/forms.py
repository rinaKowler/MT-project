from django import forms
from django.forms import ModelForm
from .models import Students

class StudentsForm(ModelForm):
    class Meta:
        model = Students
        fields = ['first_name','last_name','talents_and_level'  
        ]