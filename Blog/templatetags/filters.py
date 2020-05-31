from django import template


register = template.Library()

def title_filter(value):
    return value[0:50]+"..."

register.filter('title_filter', title_filter)

def full_blog_title_filter(value):
    return value[0:20]+"..."

register.filter('full_blog_title_filter', full_blog_title_filter)