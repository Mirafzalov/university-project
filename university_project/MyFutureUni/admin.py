from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(CategoryUni)
admin.site.register(Faculty)
# admin.site.register(University)
admin.site.register(Major)
admin.site.register(Program)
admin.site.register(Comment)
admin.site.register(ProfileUser)
admin.site.register(Ip)



class MajorInline(admin.TabularInline):
    model = Major
    fk_name = 'university'
    extra = 1



class ProgramInline(admin.TabularInline):
    model = Program
    fk_name = 'university'
    extra = 1


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'count_views', 'count_comment')
    inlines = [MajorInline, ProgramInline]
    list_display_links = ('id', 'title')


