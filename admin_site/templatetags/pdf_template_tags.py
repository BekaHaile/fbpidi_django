from django import template

register = template.Library()

@register.simple_tag
def get_fem_emp_sum(x,y):
    if x != None and y != None:
        return int(x+y)
    else:
        return 0