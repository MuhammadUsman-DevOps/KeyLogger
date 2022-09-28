from django.contrib import admin

from KeyLogger.models import Keys, Person, AssignedKeys

admin.site.index_title = "KeyLogger Administration"
admin.site.site_title = "KeyLogger Administration"
admin.site.site_header = "KeyLogger Administration"
admin.site.register(Keys)
admin.site.register(Person)
admin.site.register(AssignedKeys)
