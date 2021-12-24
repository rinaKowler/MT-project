from os import name
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models.fields import NullBooleanField
from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from myapp.models import HotelName, NightOut, Payment, Students, Volunteer
from django.db.models import Q


def home_page(request):
    payment= Payment.objects.filter( paid=False)
    paired = get_all_paired_students(1)
    return render(request, "website/home_page.html", {
            "payments": payment,
            "paired": paired

    })

def show_night_out_arrangement(request, trip_date):
    nightout = NightOut.objects.filter(trip_date__year = trip_date[:4], trip_date__month = trip_date[4:6]
    ).all()
    return render(request,"website/night_out_hotel.html",{
        "hotel": nightout
    })



def set_hotel_arrengment(hotel_id):
    all_students = get_all_students()
    all_rooms = get_all_hotel_rooms(hotel_id)
    rooms =[]
    for room in all_rooms:
        room_students = []
        current_room = all_students
        for bed in range(room.beds):
            added_student = current_students.pop()
            room_students.add(added_student)
            prev_paired = get_all_paired_students(added_student.id)
            current_students =[new_student for new_student in current_room if new_students not in prev_paired]
        rooms.add(room_students)
    # todo:add room_students to db
    return rooms

def  get_all_students(request):
     return render (request,"website/students.html",{"name":name})

def get_all_unpaired_students(student_id):
    return None
#     return Students.objects.filter()

def get_all_paired_students(student_id):
    all_night_outs = NightOut.objects.filter(student__id = student_id)
    all_paired_students =[]
    for night_out in all_night_outs:
        students_in = NightOut.objects.filter(hotel__id = night_out.hotel.id, trip_date = night_out.trip_date).exclude(student__id = night_out.student_id)
        for paird in students_in:
            all_paired_students.append(paird.student)
    return set(all_paired_students)
        
def get_all_hotel_rooms(hotel_name):
    return HotelName.objects.filter(name =hotel_name)

def get_all_volunteer_places(volunteer_id):
    all_places = get_all_volunteer_places(volunteer_id)
    all_students=get_all_students()
    return Volunteer.objects.all()



