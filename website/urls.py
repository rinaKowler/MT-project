from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include # new


from website import views
app_name = "website"

urlpatterns = [
  
    # path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')), # new
    path("login", views.login_page, name="login"),
    path("students", views.get_all_students,name="students"),
    path("payments", views.get_all_payments,name="payments"),
    path("", views.home_page, name="home_page"),
    path("volunteer", views.valnter_places, name="volunteer"),
    path("get_night_out",views.show_night_out_arrangement, name = "night_out"),
    path("show_trip",views.get_trips , name="show_trip"),
    path("hotel",views.get_all_hotels , name="hotel"),
    path("staff",views.get_all_staff , name="staff"),
    path("events",views.get_all_events , name="events"),
    path("rooms",views.get_all_rooms , name="rooms"),
    path("add_room",views.add_room_to_hotel, name="add_room"),
    path("pick_valnter", views.pick_valnter, name="pick_volunteer"),
    path("show_picked_volunteer", views.show_picked_volunteer, name="show_picked_volunteer"),
    path("notify", views.notify, name="notify"),
    path("add_payment_to_event", views.add_payment_to_event, name="add_payment_to_event"),
    path("download_doc", views.download_doc, name="download_doc"),
    path("add_lecture", views.lecture_places, name="add_lecture"),
    path("pick_Lecture", views.pick_Lecture, name="pick_Lecture"),
    path("show_picked_lecture", views.show_picked_lecture, name="show_picked_lecture"),
    path("atten_teacher_date", views.atten_teacher_date, name="atten_teacher_date"),
    path("atendence", views.atendence, name="atendence"),
    path("show_atten", views.show_atten, name="show_atten"),
    path("show_all_atten", views.show_all_atten, name="show_all_atten"),


]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


   # path("get_all_payments/<str:amount",views.show_all_pament_payment, name = "payment"),
   # path("get_all_students/<str: first_name", views.get_all_students, name="get_all_students"),

