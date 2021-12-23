from django.db.models.fields import NullBooleanField
from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from myapp.models import HotelName, NightOut, Payment, Students


def home_page(request):
    payment= Payment.objects.filter( paid=False)
    return render(request, "website/home_page.html", {
            "payments": payment,

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

def  get_all_students():
    return Students.objects.all()

def get_all_unpaired_students(student_id):
    return None
#     return Students.objects.filter()

def get_all_paired_students(student_id):
    #all_rooms = NightOut.objects.filter(student.id = student_id)
    #all_paired_students =[]
    #for room in all_rooms:
     #   students_in = NightOut.objects.filter(hotel_room_id = room.id)
    return None
        
def get_all_hotel_rooms(hotel_name):
    return HotelName.objects.filter(name =hotel_name)


