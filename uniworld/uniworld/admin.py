from django.contrib import admin
from uniamdin import models




class AdvancedRoomAdmin(admin.ModelAdmin):
    model = models.AdvancedRoom
    list_display = ('host',)


admin.site.register(models.AdvancedRoom, AdvancedRoomAdmin)
