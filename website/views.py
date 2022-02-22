from calendar import TUESDAY, WEDNESDAY
from multiprocessing import context
from os import name
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models.fields import NullBooleanField
from django.shortcuts import get_object_or_404, render,redirect
from django.http.response import HttpResponse
from myapp.models import Event, HotelName, HotelRooms, NightOut, Payment, StudentVolunteer, Students, Volunteer,Staff,Lecture,StudentLecture,Atteendence
from django.db.models import Q
from myapp.forms import StudentsForm,PaymentsForm,VolunteerForm,HotelForm,RoomsForm,EventForm,StaffForm,StudentVForm,LectureForm
from datetime import date
from random import shuffle
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage



import csv

from django.contrib.auth.models import User

def upload(request):
    context={}
    if request.method == 'POST':
      upload_file=request.FILES['document']
      fs=FileSystemStorage()
      name=fs.save(upload_file.name,upload_file)
      context ['url']=fs.url(name)   
    return render(request,"upload.html",context)

    
def download_doc(request):
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Event Payments .csv"'

    writer = csv.writer(response)
   
    id = request.POST.get('id')
    name = Event.objects.filter(id=id).first()
    all_events = Event.objects.filter(event_name=name.event_name).all()
    sumPayed = 0
    sumUnpaid= 0

    writer.writerow([name.event_name,name.event_date])
    writer.writerow(["Company","Paid","Amount"])    
    for event in all_events:
         if event.payment.paid:
            sumPayed =sumPayed+event.payment.amount
         else:
            sumUnpaid = sumUnpaid + event.payment.amount
         writer.writerow([(event.payment.company),(event.payment.paid),(event.payment.amount)])
    sum=sumPayed+sumUnpaid
    writer.writerow(["Total Paid","Total Unpaid","Sum Total"])  
    writer.writerow([sumPayed,sumUnpaid,sum])


    return response

    
def download_doc1(request):
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Voluntter .csv"'

    writer = csv.writer(response)
   
    id = request.POST.get('id')
    name = Volunteer.objects.filter(id=id).first()
    all_volunteer = Volunteer.objects.filter(volunteer_place_name=name.volunteer_place_name).all()

    writer.writerow([name.volunteer_place_name])
    for event in all_events:
         if event.payment.paid:
            sumPayed =sumPayed+event.payment.amount
         else:
            sumUnpaid = sumUnpaid + event.payment.amount
         writer.writerow([(event.payment.company),(event.payment.paid),(event.payment.amount)])
    sum=sumPayed+sumUnpaid    
    writer.writerow(["Name","Explain"])    
    writer.writerow([(StudentVolunteer.name),(StudentVolunteer.describe)])



    return response


def login_page(request):
    return render(request,"registration/login.html")

  

@login_required
def home_page(request):
    paired = get_all_paired_students(1)
    return render(request, "website/home_page.html", {
            "paired": paired,
            "user": request.user.username if request.user else ""

    })

def get_trips(request):
    all_trips = NightOut.objects.values_list('trip_date', flat=True).distinct()
    for trip in all_trips:
        print(trip)
    return render(request,"website/show_trip.html",{
        "trips":all_trips,
         "user": request.user.username if request.user else ""

        
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
            rooms_and_stu = []
            room_ids = list(set([x.hotel.room.id for x in all_students]))
            num =1
            for room in room_ids:
                st=''
                for student in all_students:
                    if student.hotel.room.id == room:
                        st = st+ student.student.last_name +' ' + student.student.first_name +','
                rooms_and_stu.append({'id':num,'students':st})
                num = num +1
            all_dates.append({'dates':rooms_and_stu, 'id':all_students[0].id, 'hotel':all_students[0].hotel.name,
            'date':all_students[0].trip_date})
            print(all_students)
    # nightout = NightOut.objects.filter(trip_date__year = trip_date[:4], trip_date__month = trip_date[4:6]
    return render(request,"website/night_out_hotel.html",{
        "dates":all_dates,
                    "user": request.user.username if request.user else ""

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
         "user": request.user.username if request.user else ""

})

def upload_recipt(request):
    return render (request,)

def  get_all_payments(request):

    if request.method == 'POST':
        form = PaymentsForm(request.POST,request.FILES)
        if form.is_valid():
            payment = form.save()
        else :
            form=PaymentsForm()
    all_payments = Payment.objects.all()
    payment= Payment.objects.filter( paid=False)
    print(all_payments,payment )
    return render (request,"website/payments/show_payments.html",{
        "payments":all_payments,
        "payment": payment,
        "paymentsForm": PaymentsForm(),
       "user": request.user.username if request.user else ""

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
           "user": request.user.username if request.user else ""

     })

def pick_valnter(request):
    if request.method=='POST':
        description = request.POST.get('description')
        id = request.POST.getlist('id')
        from django.contrib.auth.models import User
        user = User.objects.filter(username=request.user.username).first()
        last_name = user.last_name
        first_name = user.first_name
        name = first_name + ' ' + last_name
        val = Volunteer.objects.filter(id=id[0]).first()
        val2 = Volunteer.objects.filter(id=id[1]).first() if len(id) > 1 else None

        StudentVolunteer(name=name,volunteer=val,volunteer2 = val2, describe=description).save()
    all_volunteer = Volunteer.objects.all()
    return render (request,"website/volunteer/show_volunteer_places.html",{
        "volunteer":all_volunteer,
         "volunteersForm": VolunteerForm(),
         "user": request.user.username if request.user else ""

     })

def show_picked_volunteer(request):
    all = StudentVolunteer.objects.all()
    all_places1 = [x.volunteer2 for x in all]
    all_places2 = [x.volunteer for x in all]
    all_places = set([*all_places1,*all_places2])
    list_places =[]
    for place in all_places:
        print([all[0].volunteer])
        all_students = [{'name':x.name,'describe':x.describe} for x in all if x.volunteer and place and (x.volunteer.volunteer_place_name == place.volunteer_place_name  or x.volunteer2 and  x.volunteer2.volunteer_place_name == place.volunteer_place_name)]
        list_places.append({'place':place,'students':all_students})
    return render (request,"website/show_picked_volunteer.html",{
        "volunteer":list_places ,          
        "user": request.user.username if request.user else ""
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
        rooms=[h.room.number_of_beds for h in all_hotels if h.name == hotel and h.room]
        num_of_rooms = len(rooms)
        num_of_beds = sum(rooms)
        hotels_and_rooms.append({'id':id,'name':hotel,'rooms':num_of_rooms,'beds':num_of_beds})
    print(hotels_and_rooms)
    return render (request,"website/hotel/show_hotel.html",{
        "hotel":hotels_and_rooms,
        "hotelForm": HotelForm(),
        "roomsForm": RoomsForm(),
          "user": request.user.username if request.user else ""

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
         "user": request.user.username if request.user else ""

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
            payment_date=request.POST.get('payment_date'),
            recipt=request.FILES.get('document'),
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
         "user": request.user.username if request.user else ""

    })


def notify(request):
    return render(request,"website/notify.html",
    {   "user": request.user.username if request.user else ""
})


def download_doc2(request):
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
             form.save()
    all_lecture = Lecture.objects.all()
    sunday = [x for x in all_lecture if x.day == "sunday"]
    monday = [x for x in all_lecture if x.day == "monday"]
    tusday = [x for x in all_lecture if x.day == "tusday"]
    wednesday = [x for x in all_lecture if x.day == "wednesday"]
    thursday = [x for x in all_lecture if x.day == "thursday"]
    all = {'sunday':sunday,'monday':monday,'tusday':tusday,'wednesday':wednesday,'thursday':thursday }
    for a in all:
        print(all[a])
        print("----")
    print(all)
    return render (request,"website/lecture/show_lecture.html",{
        "sunday":sunday,"monday":monday,'tusday':tusday,'wednesday':wednesday,'thursday':thursday,
        "lectureForm":LectureForm(),
       "user": request.user.username if request.user else ""

     })



def pick_Lecture(request):
    if request.method=='POST':
        # name = request.POST.get('name')
        from django.contrib.auth.models import User
        user = User.objects.filter(username=request.user.username).first()
        last_name = user.last_name
        first_name = user.first_name
        name = first_name + ' ' + last_name
        s_id = request.POST.getlist('s_id')
        m_id = request.POST.getlist('m_id')
        t_id = request.POST.getlist('t_id')
        w_id = request.POST.getlist('w_id')
        th_id = request.POST.getlist('th_id')

        s_lecture =None if not s_id or len(s_id) <2 else Lecture.objects.filter(id =s_id[0]).first()
        s_lecture2 =None if not s_id or len(s_id) <2 else Lecture.objects.filter(id = s_id[1]).first()
        m_lecture =None if not m_id or len(m_id) <2 else Lecture.objects.filter(id=m_id[0]).first()
        m_lecture2 =None if not m_id or len(m_id) <2 else Lecture.objects.filter(id = m_id[1]).first()
        t_lecture =None if not t_id or len( t_id) <2 else Lecture.objects.filter(id = t_id[0]).first()
        t_lecture2 =None if not  t_id or len( t_id) <2 else Lecture.objects.filter(id = t_id[1]).first()
        w_lecture =None if not w_id or len(w_id) <2 else Lecture.objects.filter(id =w_id[0]).first()
        w_lecture2 =None if not w_id or len(w_id) <2 else Lecture.objects.filter(id = w_id[1]).first()
        th_lecture =None if not th_id or len(th_id) <2 else Lecture.objects.filter(id =th_id[0]).first()
        th_lecture2 =None if not th_id or len(th_id) <2 else Lecture.objects.filter(id = th_id[1]).first()
        StudentLecture(name=name,sunday_lecture1=s_lecture,sunady_lecture2 = s_lecture2,m1=m_lecture,m2=m_lecture2,t1=t_lecture,t2=t_lecture2,w1=w_lecture,w2=w_lecture2,th1=th_lecture,th2=th_lecture2).save()
    all_lecture = Lecture.objects.all()
    sunday = [x for x in all_lecture if x.day == "sunday"]
    monday = [x for x in all_lecture if x.day == "monday"]
    tusday = [x for x in all_lecture if x.day == "tusday"]
    wednesday = [x for x in all_lecture if x.day == "wednesday"]
    thursday = [x for x in all_lecture if x.day == "thursday"]
    all = {'sunday':sunday,'monday':monday,'tusday':tusday,'wednesday':wednesday,'thursday':thursday }
    for a in all:
        print(all[a])
        print("----")
    print(all)
    return render (request,"website/lecture/show_lecture.html",{
        "sunday":sunday,"monday":monday,'tusday':tusday,'wednesday':wednesday,'thursday':thursday,
        "lectureForm":LectureForm(),
         "user": request.user.username if request.user else ""

     })

def show_picked_lecture(request):	
    if request.method=='POST' and not request.POST.get('days'):
        name_list = request.POST.getlist('id')
        lecture_id  = request.POST.get('lecture_id')
        lec = Lecture.objects.filter(id=lecture_id).first()
        for name in name_list:
            Atteendence(name =name,
            lecture=lec ,attendence = True).save()
        return atendence(request)
    day = request.POST.get('days')
    name = request.POST.get('teacher')
    lecture = Lecture.objects.filter(teacher=name,day=day).first().id
    all = StudentLecture.objects.all()
    s = [None ] if day != 'sunday' else [x for x in all if x.sunday_lecture1 and x.sunday_lecture1.id == lecture or x.sunady_lecture2 and x.sunady_lecture2.id== lecture]
    m  = [None] if day != 'monday' else [x for x in all if x.m1 and x.m1.id == lecture or x.m2 and x.m2.id == lecture]
    t = [None] if day != 'tusday' else [x for x in all if x.t1 and x.t1.id == lecture or x.t2 and x.t2.id == lecture]
    w = [None] if day != 'wednsday' else [x for x in all if x.w1 and x.w1.id == lecture or x.w2 and  x.w2.id == lecture]
    th = [None] if day != 'thursday' else [x for x in all if x.th1 and x.th1.id == lecture or x.th2 and x.th2.id== lecture]
    students =[*s,*m,*t,*w,*th]
    students = [x for x in students if x]
    return render (request,"website/show_picked_lecture.html",{
        "lecture":students,
        "lecture_id": lecture ,
         "user": request.user.username if request.user else ""
})

def atten_teacher_date(request):
    if request.method=='POST':
        return show_picked_lecture(request)
    all = Lecture.objects.all()
    all = list(set([x.teacher for x in all]))
    return render (request,"website/atten_teacher_date.html",{
    "teachers":all,
     "user": request.user.username if request.user else ""
 })

def atendence(request):
    return render (request,"website/atendence.html")

def show_atten(request):
    if request.method=='POST':
        return show_all_atten(request)
    all = Lecture.objects.all()
    all = list(set([x.teacher for x in all]))
    return render (request,"website/show_atten.html",{
    "teachers":all ,
    "user": request.user.username if request.user else ""
})

def show_all_atten(request):

    import sys
    from django.contrib.auth.models import User
    user = User.objects.filter(username=request.user.username).first()
    print(user.last_name)
    last_name = user.last_name
    first_name = user.first_name
    day = request.POST.get('days')
    name = request.POST.get('teacher')
    print("name",first_name + ' ' + last_name)
    if request.user.username == 'kowler':
        all = Atteendence.objects.filter(lecture__teacher=name,lecture__day=day)
    else:
        all = Atteendence.objects.filter(name =first_name + ' ' + last_name,lecture__teacher=name,lecture__day=day)
        print("all",all)
        all = Atteendence.objects.filter(name =first_name + ' ' + last_name)

    all_dates = len(list(set([x.date.strftime("%m/%d/%Y, %H:%M") for x in all])))
    print(all_dates)
    all_atend =[x.name for x in all if x.attendence]
    print(all_atend)
    all_atend = [{'StudentName':x,'ClassesAtended':all_dates-all_atend.count(x)} for x in list(set(all_atend))]
    return render (request,"website/show_all_atten.html",{
    "all_dates":all_dates,
    "all_atend":all_atend,
 "user": request.user.username if request.user else ""

     })

def edit_item(request,pk,model,cls):
    item= get_object_or_404(model,pk=pk)

    if request.method=="POST":
        form=cls(request.POTS,intsrance=item)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form=cls(instance=item)
        return render (request,'edit.html',{'form':form})

def edit_payment (request,pk):
    return edit_item (request,pk,Payment,PaymentsForm)
