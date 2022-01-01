from os import name
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models.fields import NullBooleanField
from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from myapp.models import Event, HotelName, HotelRooms, NightOut, Payment, Students, Volunteer,Staff
from django.db.models import Q
from myapp.forms import StudentsForm,PaymentsForm,VolunteerForm,HotelForm,RoomsForm,EventForm,StaffForm
from datetime import date


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
    if request.method == 'POST':
        hotel_name = request.POST.get('hotel_name')
        set_hotel_arrengment(hotel_name)
    nightout = NightOut.objects.all()
    all_dates =[]
    if nightout:
        dates = set([night.trip_date for night in nightout])
        for date in dates:
            all_students = [night for night in nightout if night.trip_date == date]
            all_dates.append({'dates':all_students, 'id':all_students[0].id, 'hotel':all_students[0].hotel.name,
            'date':all_students[0].trip_date})
        print(all_dates)
    # nightout = NightOut.objects.filter(trip_date__year = trip_date[:4], trip_date__month = trip_date[4:6]
    return render(request,"website/night_out_hotel.html",{
        "dates":all_dates
    })



def set_hotel_arrengment(hotel_name):
    all_students =[student for student in Students.objects.all()]
    all_rooms = get_all_hotel_rooms(hotel_name)
    rooms =[]


    for room in all_rooms:
        room_students = []
        current_room = all_students
        if current_room:
            for bed in range(int(room.room.number_of_beds)) :
                if current_room and all_students: 
                    added_student = current_room.pop()
                    all_students = [student for student in all_students if student != added_student]

                    room_students.append(added_student)
                    prev_paired = get_all_paired_students(added_student.id)
                    print(prev_paired)
                    current_room =[new_student for new_student in current_room if new_student not in prev_paired]
            rooms.append({'room_id':room.room.id,'students':room_students})    
    for room in rooms:
        hotel =HotelName.objects.filter(name=hotel_name ,room_id =room['room_id']).first()        
        for student in room['students']:

            NightOut(student=student, hotel=hotel, trip_date= date.today()).save()

    # todo:add room_students to db
    return rooms


        
def get_all_unpaired_students(student_id):
    return None
    return Students.objects.filter(),



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
     } ) 

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
    all_hotel_names = set([h.name for h in all_hotels])
    print(all_hotels)
    hotels_and_rooms =[]
    for hotel in all_hotel_names:
        id =  [h.id for h in all_hotels if h.name ==hotel][0]
        hotels_and_rooms.append({'name':hotel,'rooms':[h.room.number_of_beds for h in all_hotels if h.name == hotel and h.room]})
    print(hotels_and_rooms)
    return render (request,"website/hotel/show_hotel.html",{
        "hotel":hotels_and_rooms,
        "hotelForm": HotelForm(),
        "roomsForm": RoomsForm()
    })

def add_room_to_hotel(request):
    if request.method == 'POST':
        hotel_name = request.POST.get('hotel_name')
        rooms = request.POST.get('number_of_beds')
        room = HotelRooms(number_of_beds = rooms)
        room.save()
        hotel = HotelName(name=hotel_name,room=room)
        hotel.save()
    return get_all_hotels(request)

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
    print( all_rooms)
    return get_all_hotels()
    

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