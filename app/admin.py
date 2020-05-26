from django.contrib import admin

# Register your models here.
from app.models import *

# Register your models here.
admin.site.register(Event)
admin.site.register(Department)
admin.site.register(Project)
admin.site.register(Section)
admin.site.register(Progress)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Problem)