import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Word


def create_word(word, definition="A test definition.", days=0):
    """
    Creates a saved word. `days` moves the save date:
    negative for words saved in the past.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Word.objects.create(word=word, definition=definition, date_saved=time)


class SearchPageTests(TestCase):
    def test_search_page_shows_the_form(self):
        """The search page loads and shows the search form."""
        response = self.client.get(reverse("dictionary:search_page"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form>")


class WordListViewTests(TestCase):
    def test_no_saved_words(self):
        """If no words are saved, a message is displayed."""
        response = self.client.get(reverse("dictionary:word_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No words saved yet.")
        self.assertQuerySetEqual(response.context["saved_words"], [])

    def test_newest_words_first(self):
        """The most recently saved word is shown first."""
        older_word = create_word("apple", days=-2)
        newer_word = create_word("banana", days=-1)
        response = self.client.get(reverse("dictionary:word_list"))
        self.assertQuerySetEqual(
            response.context["saved_words"], [newer_word, older_word]
        )


class WordDetailViewTests(TestCase):
    def test_word_that_does_not_exist(self):
        """Asking for an id that is not in the database returns a 404."""
        response = self.client.get(reverse("dictionary:word_detail", args=(999,)))
        self.assertEqual(response.status_code, 404)

    def test_saved_word(self):
        """The detail page shows the word and its definition."""
        saved_word = create_word("apple", "The fruit of an apple tree.")
        response = self.client.get(
            reverse("dictionary:word_detail", args=(saved_word.id,))
        )
        self.assertContains(response, "apple")
        self.assertContains(response, "The fruit of an apple tree.")


class DeleteWordTests(TestCase):
    def test_delete_word(self):
        """Deleting a word removes it and redirects to My Vocabulary."""
        saved_word = create_word("apple")
        response = self.client.post(
            reverse("dictionary:delete_word", args=(saved_word.id,))
        )
        self.assertRedirects(response, reverse("dictionary:word_list"))
        self.assertFalse(Word.objects.filter(pk=saved_word.id).exists())
