import django
import os
import sys

from django.db.models import Q
from django.utils import timezone


sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wey_backend.settings")
django.setup()

from account.models import User

users = User.objects.all()

for user in users:
    # Clear the suggestion list
    user.people_you_may_know.clear()

    print('Find friends for:', user)

    # Get friends' IDs
    friend_ids = user.friends.values_list('id', flat=True)

    # Find friends of friends who are not already friends with the user
    friends_of_friends = User.objects.filter(
        friends__in=friend_ids
    ).exclude(
        Q(friends=user) | Q(id=user.id)
    ).distinct()

    # Add friends of friends to "people_you_may_know" for the user
    user.people_you_may_know.set(friends_of_friends)

    print()