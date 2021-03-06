from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from website import views
app_name = "website"

urlpatterns = [
    path("students", views.get_all_students,name="students"),
    path("payments", views.get_all_payments,name="payments"),
    path("", views.home_page, name="home_page"),
    path("volunteer", views.valnter_places, name="volunteer"),
    path("get_night_out",views.show_night_out_arrangement, name = "night_out"),
    path("show_trip",views.get_trips , name="show_trip")
   # path("get_all_payments/<str:amount",views.show_all_pament_payment, name = "payment"),
   # path("get_all_students/<str: first_name", views.get_all_students, name="get_all_students"),
]
