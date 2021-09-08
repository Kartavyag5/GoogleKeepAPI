from django.contrib import admin
from .models import *
# Register your models here.

class ClientDetailsAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(ClientDetailsAdmin, self).get_changeform_initial_data(request)
        get_data['User'] = request.user.pk
        return get_data

admin.site.register(Note)
admin.site.register(List)
admin.site.register(Image,ClientDetailsAdmin)
admin.site.register(Extendeduser)
admin.site.register(ListItem)
admin.site.register(ImageList)


