from pickle import TRUE
from django.db import models
from datetime import datetime, date
from django.utils import timezone
from django import forms
from .models import *
from django.db.models.fields.related import ForeignKey
## from myapp.views import payment



class HotelName(models.Model):
    name= models.CharField(max_length=20)
    room = models.ForeignKey(
        'HotelRooms', on_delete=models.RESTRICT, null=True, blank=True)
    def _str_ (self):
         return self.name 

class HotelRooms(models.Model):
    number_of_beds=models.IntegerField( null=True, blank=True)

class NightOut(models.Model):
    trip_date =models.DateField()  
    hotel = models.ForeignKey(
        'HotelName', on_delete=models.RESTRICT, null=True, blank=True)
    student = models.ForeignKey(
        'Students', on_delete=models.RESTRICT, null=True, blank=True)
      

class Students(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email=models.EmailField(max_length=254,blank=True,null=True)
    phone =models.IntegerField(null=True)

    def _str_ (self):
         return self.first_name +' '+ self.last_name


class Event (models.Model):
    event_name=models.CharField(max_length=50)
    place=models.CharField(max_length=200,blank=True,null=True)
    manager=models.CharField(max_length=50,blank=True,null=True)
    event_date=models.DateField(auto_now=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.RESTRICT, null=True, blank=True)
    
    def _str_ (self):
         return self.event_name 

class Payment (models.Model):
    company=models.CharField(max_length=200)
    purchased_date=models.DateField(auto_now=True, blank=True)
    managed_by=models.CharField(max_length=50, null=True, blank=True)
    description=models.TextField(max_length=400, null=True, blank=True)
    amount=models.IntegerField( null=True)
    paid= models.BooleanField(default=False)
    if_not_way=models.TextField(max_length=400, null=True, blank=True)
    payment_date=models.DateTimeField( null=True, blank=True)
    
    def _str_ (self):
         return self.company +' '+ self.payment_date
        
class Staff(models.Model):
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    title=models.CharField(max_length=200)
    email = models.EmailField( blank=True)

class Volunteer(models.Model):
    category=models.CharField(max_length=200)
    volunteer_place_name=models.CharField(max_length=200) 
    address=models.CharField(max_length=200)
    describe= models.TextField(max_length=500)



class StudentVolunteer(models.Model):
    name=models.CharField(max_length=50)
    volunteer = models.ForeignKey(
        'Volunteer', on_delete=models.RESTRICT, null=True, blank=True)
    volunteer2 = models.ForeignKey(
        'Volunteer', related_name='volunteer2', on_delete=models.RESTRICT, null=True, blank=True)
    describe=models.CharField(max_length=200)

class Lecture(models.Model):
    subject=models.CharField(max_length=50)
    teacher=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    time=models.CharField(max_length=50,null=True, blank=True)

class Atteendence(models.Model):
    name =models.CharField(max_length=50)
    date =models.DateTimeField(auto_now=True, null=True, blank=True)
    lecture=models.ForeignKey(
        'lecture', on_delete=models.RESTRICT, null=True, blank=True)
    attendence=models.BooleanField(default=False)

class StudentLecture(models.Model):
    name=models.CharField(max_length=50)
    sunday_lecture1 = models.ForeignKey(
        'lecture',related_name='sunday_lecture1', on_delete=models.RESTRICT, null=True, blank=True)
    sunady_lecture2 = models.ForeignKey(
        'lecture', related_name='sunday_lecture2', on_delete=models.RESTRICT, null=True, blank=True)
    m1 = models.ForeignKey(
        'lecture',related_name='m1', on_delete=models.RESTRICT, null=True, blank=True)
    m2 = models.ForeignKey(
        'lecture', related_name='m2', on_delete=models.RESTRICT, null=True, blank=True)
    t1 = models.ForeignKey(
        'lecture',related_name='t1', on_delete=models.RESTRICT, null=True, blank=True)
    t2 = models.ForeignKey(
        'lecture', related_name='t2', on_delete=models.RESTRICT, null=True, blank=True)
    w1 = models.ForeignKey(
        'lecture',related_name='w1', on_delete=models.RESTRICT, null=True, blank=True)
    w2 = models.ForeignKey(
        'lecture', related_name='w2', on_delete=models.RESTRICT, null=True, blank=True)
    th1 = models.ForeignKey(
        'lecture',related_name='th1', on_delete=models.RESTRICT, null=True, blank=True)
    th2 = models.ForeignKey(
        'lecture', related_name='th2', on_delete=models.RESTRICT, null=True, blank=True)
      