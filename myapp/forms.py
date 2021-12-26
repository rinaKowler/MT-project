from django import forms
from django.forms import ModelForm
from .models import Students ,Payment, Volunteer


class StudentsForm(ModelForm):
    class Meta:
        model = Students
        fields = ['first_name','last_name','talents_and_level'  
        ]
class PaymentsForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['amount','company','managed_by','description','if_not_way'
]
   
class VolunteerForm(ModelForm):
    class Meta:
        model = Volunteer
        fields = ['category','volunteer_place_name','address','describe']
     
