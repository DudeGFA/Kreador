from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i].image.url

@register.filter
def calc_total_votes(pollobject):
    total_votes = 0
    for polloption in pollobject.polloption_set.all():
        total_votes += polloption.voters.count()
    return total_votes