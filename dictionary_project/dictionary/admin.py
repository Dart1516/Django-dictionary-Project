from django.contrib import admin

from .models import Word

# Makes the Word model visible in the admin site (/admin/),
# so words can be added, edited and deleted from there.
admin.site.register(Word)
