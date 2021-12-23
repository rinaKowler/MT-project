
from django.contrib import admin

from .models import Event, HotelName, HotelRooms, NightOut, Students,Payment,Staff,Volunteer
admin.site.register(Students)
admin.site.register(Event)
admin.site.register(Payment)
admin.site.register(HotelName)
admin.site.register(HotelRooms)
admin.site.register(NightOut)
admin.site.register(Staff)
admin.site.register(Volunteer)



