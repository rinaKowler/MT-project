from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from website import views
app_name = "website"

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("get_night_out/<str:trip_date>",views.show_night_out_arrangement, name = "night_out"),
   # path("get_all_payments/<str:amount",views.show_all_pament_payment, name = "payment"),
   
]