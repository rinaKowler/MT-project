from django import forms
from django.forms import ModelForm
from .models import Staff, Students ,Payment, Volunteer,Event,HotelName,HotelRooms,Staff,StudentVolunteer
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, HTML


class DateInput(forms.DateInput):
    input_type= 'event_date'

class ExampleForm(forms.Form):
    event_date= forms.DateField(widget=DateInput)
   


class StudentsForm(ModelForm):
    class Meta:
        model = Students
        fields = {'first_name','last_name','email'}
        widgets = {
            'first_name': forms.TextInput(),  
            'last_name': forms.TextInput(),
            'talents_and_level': forms.TextInput(),
        }
          
class PaymentsForm(ModelForm):
    
    paid = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = Payment
        fields = ['amount','company','managed_by','description','if_not_way','paid',]
        widgets = {
            'amount': forms.TextInput(),
            'company': forms.TextInput(),
            'managed_by': forms.TextInput(),
            'description': forms.TextInput(),
            'if_not_way': forms.TextInput(),

              } 
    
class VolunteerForm(ModelForm):
    class Meta:
        model = Volunteer
        fields = ['category','volunteer_place_name','address','describe',]
        widgets = {
            'category': forms.TextInput(),
            'volunteer_place_name': forms.TextInput(),
            'address': forms.TextInput(),
            'describe': forms.TextInput(),
        
              } 
        
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['event_name','place','manager','payment']
        widgets={'date':forms.DateInput()}

class HotelForm(ModelForm):
    class Meta:
        model = HotelName
        fields = ['name']
        
class RoomsForm(ModelForm):
    class Meta:
        model = HotelRooms
        fields = ['number_of_beds']
    
class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name','last_name','title','email']    

     
class StudentVForm(ModelForm):
    class Meta:
        model = StudentVolunteer
        fields = ['name','describe']      


