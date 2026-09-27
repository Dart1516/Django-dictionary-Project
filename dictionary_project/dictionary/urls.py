from django.urls import path

from . import views

# The namespace used in templates, for example {% url 'dictionary:word_list' %}
app_name = "dictionary"

urlpatterns = [
    # /                   -> Search page
    path("", views.search_page, name="search_page"),
    # /words/             -> My Vocabulary page
    path("words/", views.WordListView.as_view(), name="word_list"),
    # /words/1/           -> Word Detail page of the word with id 1
    path("words/<int:pk>/", views.WordDetailView.as_view(), name="word_detail"),
    # /words/1/delete/    -> Deletes the word with id 1 (used by the Delete button)
    path("words/<int:word_id>/delete/", views.delete_word, name="delete_word"),
]
