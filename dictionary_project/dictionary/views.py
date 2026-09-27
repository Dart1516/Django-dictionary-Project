from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Word


def search_page(request):
    """
    Search page (/).
    For now it only shows the search form; the search is not connected yet.
    """
    return render(request, "dictionary/search.html")


class WordListView(generic.ListView):
    """
    My Vocabulary page (/words/).
    Reads every saved word from the database, newest first.
    """

    template_name = "dictionary/word_list.html"
    context_object_name = "saved_words"

    def get_queryset(self):
        return Word.objects.order_by("-date_saved")


class WordDetailView(generic.DetailView):
    """
    Word Detail page (/words/<id>/).
    Shows one saved word with all its information.
    Returns a 404 error if no word has that id.
    """

    model = Word
    template_name = "dictionary/word_detail.html"
    context_object_name = "saved_word"


def delete_word(request, word_id):
    """
    Deletes one word when the user presses the Delete button,
    then sends the user back to the My Vocabulary page.
    """
    saved_word = get_object_or_404(Word, pk=word_id)
    saved_word.delete()
    # Redirect after a POST, so the Back button does not send the form again.
    return HttpResponseRedirect(reverse("dictionary:word_list"))
