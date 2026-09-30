from django.urls import path

from . import views

# Used in templates like {% url 'dictionary:word_list' %}
app_name = "dictionary"

urlpatterns = [
    # Search page
    path("", views.search_page, name="search_page"),
    # Save button
    path("save/", views.save_word, name="save_word"),
    # My Vocabulary page
    path("words/", views.WordListView.as_view(), name="word_list"),
    # Detail page, for example /words/1/
    path("words/<int:pk>/", views.WordDetailView.as_view(), name="word_detail"),
    # Mark as learned / pending button
    path("words/<int:word_id>/learned/", views.toggle_learned, name="toggle_learned"),
    # Delete button
    path("words/<int:word_id>/delete/", views.delete_word, name="delete_word"),
]
