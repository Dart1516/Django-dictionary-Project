import requests
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Word

DATAMUSE_URL = "https://api.datamuse.com/words"


# Calls Datamuse and returns (word, definition), or None if the word doesn't exist
def get_definition_from_datamuse(searched_word):
    response = requests.get(
        DATAMUSE_URL,
        params={"sp": searched_word, "md": "d", "max": 1},
        timeout=5,
    )
    response.raise_for_status()
    results = response.json()

    if not results or "defs" not in results[0]:
        return None

    # Definitions come like "n\tdefinition", so I keep only the text after the tab
    definition = results[0]["defs"][0].split("\t", 1)[-1].strip()
    return results[0]["word"], definition


# Search page: reads the word from the URL (?word=apple) and shows its definition
def search_page(request):
    searched_word = request.GET.get("word", "").strip()
    context = {"searched_word": searched_word}

    if searched_word:
        try:
            result = get_definition_from_datamuse(searched_word)
        except requests.RequestException:
            context["error_message"] = "Could not connect to the dictionary. Try again later."
            return render(request, "dictionary/search.html", context)

        if result is None:
            context["error_message"] = f'No definition found for "{searched_word}".'
        else:
            found_word, definition = result
            context["found_word"] = found_word
            context["definition"] = definition
            context["already_saved"] = Word.objects.filter(word=found_word).exists()

    return render(request, "dictionary/search.html", context)


# Save button: saves the word (only once) and opens its detail page
def save_word(request):
    try:
        word_text = request.POST["word"]
        definition = request.POST["definition"]
    except KeyError:
        return HttpResponseRedirect(reverse("dictionary:search_page"))

    saved_word, created = Word.objects.get_or_create(
        word=word_text, defaults={"definition": definition}
    )
    return HttpResponseRedirect(reverse("dictionary:word_detail", args=(saved_word.id,)))


# My Vocabulary page: all saved words
class WordListView(generic.ListView):
    template_name = "dictionary/word_list.html"
    context_object_name = "saved_words"

    # Newest words first
    def get_queryset(self):
        return Word.objects.order_by("-date_saved")


# Detail page of one word (404 if the id doesn't exist)
class WordDetailView(generic.DetailView):
    model = Word
    template_name = "dictionary/word_detail.html"
    context_object_name = "saved_word"


# Learned button: switches between Learned and Pending
def toggle_learned(request, word_id):
    saved_word = get_object_or_404(Word, pk=word_id)
    saved_word.is_learned = not saved_word.is_learned
    saved_word.save()
    return HttpResponseRedirect(reverse("dictionary:word_detail", args=(saved_word.id,)))


# Delete button: deletes the word and goes back to My Vocabulary
def delete_word(request, word_id):
    saved_word = get_object_or_404(Word, pk=word_id)
    saved_word.delete()
    return HttpResponseRedirect(reverse("dictionary:word_list"))
