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

@register.filter
def comment_query_set_slice(comment_query_set):
    if comment_query_set.count() > 10:
        return comment_query_set[:10]
    return comment_query_set

@register.filter
def reply_query_set_slice(reply_query_set):
    if reply_query_set.count() > 5:
        return reply_query_set[:5]
    return reply_query_set