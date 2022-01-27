from os import name
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models.fields import NullBooleanField
from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from myapp.models import Event, HotelName, HotelRooms, NightOut, Payment, StudentVolunteer, Students, Volunteer,Staff,Lecture,StudentLecture
from django.db.models import Q
from myapp.forms import StudentsForm,PaymentsForm,VolunteerForm,HotelForm,RoomsForm,EventForm,StaffForm,StudentVForm,LectureForm
from datetime import date
from random import shuffle
from django.contrib.auth.decorators import login_required
import xlwt


@login_required
def home_page(request):
    paired = get_all_paired_students(1)
    return render(request, "website/home_page.html", {
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
    shuffle(all_students)
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
    return HotelName.objects.filter(name =hotel_name).exclude(room__isnull=True)

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
    payment= Payment.objects.filter( paid=False)

    return render (request,"website/payments/show_payments.html",{
        "payments":all_payments,
        "payment": payment,
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

def pick_valnter(request):
    if request.method=='POST':
        description = request.POST.get('description')
        id = request.POST.getlist('id')
        name = request.POST.get('name')
        val = Volunteer.objects.filter(id=id[0]).first()
        val2 = Volunteer.objects.filter(id=id[1]).first()

        StudentVolunteer(name=name,volunteer=val,volunteer2 = val2, describe=description).save()
    all_volunteer = Volunteer.objects.all()
    return render (request,"website/volunteer/show_volunteer_places.html",{
        "volunteer":all_volunteer,
         "volunteersForm": VolunteerForm(),
     })

def show_picked_volunteer(request):
    all = StudentVolunteer.objects.all()
    all_places1 = [x.volunteer2 for x in all]
    all_places2 = [x.volunteer for x in all]
    all_places = set([*all_places1,*all_places2])
    list_places =[]
    for place in all_places:
        print([all[0].volunteer])
        all_students = [x.name for x in all if x.volunteer.volunteer_place_name == place.volunteer_place_name  or x.volunteer2.volunteer_place_name == place.volunteer_place_name]
        list_places.append({'place':place,'students':all_students})
    return render (request,"website/show_picked_volunteer.html",{
        "volunteer":list_places })

        
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
        hotels_and_rooms.append({'id':id,'name':hotel,'rooms':[h.room.number_of_beds for h in all_hotels if h.name == hotel and h.room]})
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
    all_events_names = set([h.event_name for h in all_events])
    events_and_payments = []
    for event in all_events_names:
        payments =  [h.payment for h in all_events if h.event_name ==event]
        event = [h for h in all_events if h.event_name ==event][0]
        events_and_payments.append( {'event':event,'payments':payments})
    return render (request,"website/events/show_events.html",{
        "event":events_and_payments,
        "eventForm": EventForm(),
        "paymentForm":PaymentsForm(),
    })

def add_payment_to_event(request):
    if request.method == 'POST':
        print(request.POST)
        event_id = request.POST.get('event_id')
        # payment = PaymentsForm(request.POST)
        # if payment.is_valid():
        #     new_payment = payment.save()
        # print(payment)
        new_payment = Payment(
            company=request.POST.get('company'),
            purchased_date=request.POST.get('purchased_date'),
            managed_by=request.POST.get('managed_by'),
            description=request.POST.get('description'),
            amount=request.POST.get('amount'),
            paid=True if request.POST.get('paid') == 'on' else False,
            if_not_way=request.POST.get('if_not_way'),
            payment_date=request.POST.get('payment_date')
            )
        new_payment.save()
        event = Event.objects.filter(id=event_id).first()
        new_event = Event( event_name=event.event_name,
          
            event_date=event.event_date,
            payment = new_payment)
        event.payment = new_payment
        new_event.save()
    return get_all_events(request)



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


def notify(request):
    return render(request,"website/notify.html")

def download_doc(request):
    id = request.POST.get('id')
    name = Event.objects.filter(id=id).first()
    all_events = Event.objects.filter(event_name=name.event_name).all()
    # for event in all_events_names:
    #     payments =  [h.payment for h in all_events if h.event_name ==event]
    #     event = [h for h in all_events if h.event_name ==event][0]
    #     events_and_payments.append( {'event':event,'payments':payments})
    file_name = 'students.txt'
    lines = []
    lines.append('{0}, {1}, {2}'.format("company","paid","amount"))
    for p in all_events:
        lines.append('{0}, {1}, {2}'.format(p.payment.company,p.payment.paid,p.payment.amount))
    lines.append('')
    sumPayed = 0
    sumUnpaid= 0
    for event in all_events:
        if event.payment.paid:
            sumPayed =sumPayed+event.payment.amount
        else:
            sumUnpaid = sumUnpaid + event.payment.amount
    lines.append(f"""sumPayed:{sumPayed} """)
    lines.append(f"""sumUnpaid:{sumUnpaid} """)
    lines.append(f"""Total:{sumUnpaid +sumPayed } """)
    response_content = '\n'.join(lines)
    response = HttpResponse(response_content, content_type="text/plain,charset=utf8")
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
    return response


 
def lecture_places(request):
    if request.method == 'POST':
         form = LectureForm(request.POST)
         if form.is_valid():
             lecture = form.save()
    all_lecture = Lecture.objects.all()
    return render (request,"website/lecture/show_lecture.html",{
        "lecture":all_lecture,
         "lectureForm": LectureForm(),
     })
   


def pick_Lecture(request):
    if request.method=='POST':
        description = request.POST.get('subject')
        id = request.POST.getlist('id')
        teacher = request.POST.get('teacher')
        lecture = Lecture.objects.filter(id=id[0]).first()
        lecture2 = Lecture.objects.filter(id=id[1]).first()

        StudentLecture(teacher=teacher,lecture=lecture,lecture2 = lecture2, describe=description).save()
    all_lecture = Lecture.objects.all()
    return render (request,"website/lecture/show_lecture.html",{
        "lecture":all_lecture,
        "lectureForm":LectureForm(),
     })

def show_picked_lecture(request):
    all = StudentLecture.objects.all()
    all_lecture1 = [x.lecture2 for x in all]
    all_lecture2 = [x.lecture for x in all]
    all_places = set([*all_lecture1,*all_lecture2])
    list_lecture =[]
    for lecture in all_lecture:
        print([all[0].lecture])
        all_students = [x.name for x in all if x.lecture.lecture == place.volunteer_place_name  or x.volunteer2.volunteer_place_name == place.volunteer_place_name]
        list_places.append({'place':place,'students':all_students})
    return render (request,"website/show_picked_lecture.html",{
        "lecture":list_places })

    