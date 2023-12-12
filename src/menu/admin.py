from django.contrib import admin
from .models import MenuItem


@admin.register(MenuItem)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    fields = ['name', 'parent']
