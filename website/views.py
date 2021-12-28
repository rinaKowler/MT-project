from os import name
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models.fields import NullBooleanField
from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from myapp.models import Event, HotelName, HotelRooms, NightOut, Payment, Students, Volunteer,Staff
from django.db.models import Q
from myapp.forms import StudentsForm,PaymentsForm,VolunteerForm,HotelForm,RoomsForm,EventForm,StaffForm



def home_page(request):
    payment= Payment.objects.filter( paid=False)
    paired = get_all_paired_students(1)
    return render(request, "website/home_page.html", {
            "payments": payment,
            "paired": paired

    })

def get_trips(request):
    all_trips = NightOut.objects.values_list('trip_date', flat=True).distinct()
    for trip in all_trips:
        print(trip)
    return render(request,"website/show_trip.html",{
        "trips":all_trips
    })

def show_night_out_arrangement(request):
    nightout = NightOut.objects.all()
    all_dates =[]
    if nightout:
        dates = set([night.trip_date for night in nightout])
        all_dates =[]
        for date in dates:
            dates = [night for night in nightout if night.trip_date == date]
            all_dates.append({'dates':dates, 'id':dates[0].id, 'hotel':dates[0].hotel.name,
            'date':dates[0].trip_date})
        print(all_dates)
    # nightout = NightOut.objects.filter(trip_date__year = trip_date[:4], trip_date__month = trip_date[4:6]
    return render(request,"website/night_out_hotel.html",{
        "dates":all_dates
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
    if request.method == 'POST':
        form = StudentsForm(request.POST)
        if form.is_valid():
            student = form.save()
    all_students = Students.objects.all()
    return render (request,"website/students/show_students.html",{
        "students":all_students,
        "studentsForm": StudentsForm(),
})


def  get_all_payments(request):
    if request.method == 'POST':
        form = PaymentsForm(request.POST)
        if form.is_valid():
            payment = form.save()
    all_payments = Payment.objects.all()
    return render (request,"website/payments/show_payments.html",{
        "payments":all_payments,
        "paymentsForm": PaymentsForm(),
})

def get_all_unpaired_students(student_id):
    return None
    return Students.objects.filter() 

def valnter_places(request):
    if request.method == 'POST':
         form = VolunteerForm(request.POST)
         if form.is_valid():
             volunteer = form.save()
    all_volunteer = Volunteer.objects.all()
    return render (request,"website/volunteer/show_volunteer_places.html",{
        "volunteer":all_volunteer,
         "volunteersForm": VolunteerForm(),
  
})
def  get_all_hotels(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            hotel = form.save()
    all_hotels = HotelName.objects.all()
    return render (request,"website/hotel/show_hotel.html",{
        "hotel":all_hotels,
        "hotelForm": HotelForm(),
    })

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

def get_all_rooms(request):   
    if request.method == 'POST':
        form = RoomsForm(request.POST)
        if form.is_valid():
            room = form.save()
    all_rooms =HotelRooms.objects.all()
    return render (request,"website/hotel/add_rooms.html",{
        "room":all_rooms,
        "roosmForm": RoomsForm(),

    })
def  get_all_events(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
    all_events = Event.objects.all()
    return render (request,"website/events/show_events.html",{
        "event":all_events,
        "eventForm": EventForm(),
    })
   
def  get_all_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            staff = form.save()
    all_staff = Staff.objects.all()
    return render (request,"website/staff/show_staff.html",{
        "staff":all_staff,
        "staffForm": StaffForm(),
    })