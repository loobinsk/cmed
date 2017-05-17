from django import template

from ..models import SocialIcons

register = template.Library()
@register.assignment_tag
def socials():
    a = SocialIcons.objects.filter(active=True).values('name', 'icon', 'url')
    return a