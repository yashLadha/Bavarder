from django import template

register = template.Library()


@register.filter(name='addcss')
def addcss(field, args):
    value_arr = [arg.strip() for arg in args.split(',')]
    return field.as_widget(attrs={"class": value_arr[0], "placeholder": value_arr[1]})
