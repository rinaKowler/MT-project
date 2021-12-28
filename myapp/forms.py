from django import forms
from django.forms import ModelForm
from .models import Staff, Students ,Payment, Volunteer,Event,HotelName,HotelRooms,Staff

class DateInput(forms.DateInput):
    input_type= 'event_date'

class ExampleForm(forms.Form):
    event_date= forms.DateField(widget=DateInput)


class StudentsForm(ModelForm):
    class Meta:
        model = Students
        fields = ['first_name','last_name','talents_and_level'  
        ]
class PaymentsForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['amount','company','managed_by','description','if_not_way']
    
class VolunteerForm(ModelForm):
    class Meta:
        model = Volunteer
        fields = ['category','volunteer_place_name','address','describe']
        
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['event_name','place','manager','payment']
        widgets={'date':DateInput}

class HotelForm(ModelForm):
    class Meta:
        model = HotelName
        fields = ['name','room']
class RoomsForm(ModelForm):
    class Meta:
        model = HotelRooms
        fields = ['number_of_beds']
    
class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name','last_name','title','email']    

    
