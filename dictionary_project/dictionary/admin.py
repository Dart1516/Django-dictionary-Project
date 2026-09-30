from django.contrib import admin

from .models import Word


# Columns, filter and search box for words in /admin/
class WordAdmin(admin.ModelAdmin):
    list_display = ["word", "date_saved", "is_learned"]
    list_filter = ["is_learned", "date_saved"]
    search_fields = ["word"]


admin.site.register(Word, WordAdmin)
