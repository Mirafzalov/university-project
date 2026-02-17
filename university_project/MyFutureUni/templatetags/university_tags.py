from MyFutureUni.models import CategoryUni, Faculty
from django import template

register = template.Library()

@register.simple_tag()
def get_categories():
    categories = CategoryUni.objects.all()
    return categories


@register.simple_tag()
def get_faculties():
    faculties = Faculty.objects.all()
    return faculties
