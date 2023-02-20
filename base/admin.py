from django.contrib import admin
from .models import Village, Debate, Message, User

admin.site.register(User)
admin.site.register(Village)
admin.site.register(Debate)
admin.site.register(Message)
