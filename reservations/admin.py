from django.contrib import admin
from .models import Table, Reservation
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken

admin.site.register(Table)
admin.site.register(Reservation)
