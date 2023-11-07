from django import template
register = template.Library()
from django.contrib.auth.models import User
from django.db.models import Q
from userprofile.models import Profile

@register.filter
def index(indexable, i):
    return indexable[i].image.url

@register.filter
def check_voter(post, user):
    for option in post.polloption_set.all():
        if user in option.voters.all():
            return True
    return False

@register.filter
def calc_total_votes(pollobject):
    total_votes = 0
    for polloption in pollobject.polloption_set.all():
        total_votes += polloption.voters.count()
    return total_votes

@register.filter
def calc_vote_percentage(option):
    total_votes = 0
    for polloption in option.poll.polloption_set.all():
        total_votes += polloption.voters.count()
    vote_percentage = (option.voters.count() / total_votes) * 100
    return vote_percentage

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


@register.filter
def get_shared_contacts(user, contact):
    return user.profile.contacts.all() & contact.profile.contacts.all()

@register.filter
def get_shared_contacts_summary(user, contact):
    shared_contacts = user.profile.contacts.all() & contact.profile.contacts.all()
    if shared_contacts.count() > 2:
        adjusted_count = str(shared_contacts.count() - 2)
        return shared_contacts[0].username + ', ' + shared_contacts[1].username + ' and ' + adjusted_count + ' other shared contacts'
    elif shared_contacts.count() > 1:
        return shared_contacts[0].username + ' and 1 other shared contacts'
    return 'No shared Contact'