import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Word


# Creates a word; negative days = saved in the past
def create_word(word, definition="A test definition.", days=0):
    time = timezone.now() + datetime.timedelta(days=days)
    return Word.objects.create(word=word, definition=definition, date_saved=time)


class SearchPageTests(TestCase):
    # Without a word, the page only shows the form
    def test_search_page_shows_the_form(self):
        response = self.client.get(reverse("dictionary:search_page"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="word"')
        self.assertNotContains(response, "No definition found")


class SaveWordTests(TestCase):
    # Saving a word stores it and opens its detail page
    def test_save_word(self):
        response = self.client.post(
            reverse("dictionary:save_word"),
            {"word": "apple", "definition": "The fruit of an apple tree."},
        )
        saved_word = Word.objects.get(word="apple")
        self.assertRedirects(
            response, reverse("dictionary:word_detail", args=(saved_word.id,))
        )
        self.assertEqual(saved_word.definition, "The fruit of an apple tree.")
        self.assertIs(saved_word.is_learned, False)

    # The same word is not saved twice
    def test_save_same_word_twice(self):
        data = {"word": "apple", "definition": "The fruit of an apple tree."}
        self.client.post(reverse("dictionary:save_word"), data)
        self.client.post(reverse("dictionary:save_word"), data)
        self.assertEqual(Word.objects.filter(word="apple").count(), 1)

    # Without data, nothing is saved and it goes back to Search
    def test_save_without_data(self):
        response = self.client.post(reverse("dictionary:save_word"))
        self.assertRedirects(response, reverse("dictionary:search_page"))
        self.assertEqual(Word.objects.count(), 0)


class ToggleLearnedTests(TestCase):
    # First click = Learned, second click = Pending
    def test_toggle_learned(self):
        saved_word = create_word("apple")
        url = reverse("dictionary:toggle_learned", args=(saved_word.id,))

        self.client.post(url)
        saved_word.refresh_from_db()
        self.assertIs(saved_word.is_learned, True)

        self.client.post(url)
        saved_word.refresh_from_db()
        self.assertIs(saved_word.is_learned, False)


class WordListViewTests(TestCase):
    # With no words, a message is shown
    def test_no_saved_words(self):
        response = self.client.get(reverse("dictionary:word_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No words saved yet.")
        self.assertQuerySetEqual(response.context["saved_words"], [])

    # The newest word is shown first
    def test_newest_words_first(self):
        older_word = create_word("apple", days=-2)
        newer_word = create_word("banana", days=-1)
        response = self.client.get(reverse("dictionary:word_list"))
        self.assertQuerySetEqual(
            response.context["saved_words"], [newer_word, older_word]
        )


class WordDetailViewTests(TestCase):
    # An id that doesn't exist returns 404
    def test_word_that_does_not_exist(self):
        response = self.client.get(reverse("dictionary:word_detail", args=(999,)))
        self.assertEqual(response.status_code, 404)

    # The detail page shows the word and its definition
    def test_saved_word(self):
        saved_word = create_word("apple", "The fruit of an apple tree.")
        response = self.client.get(
            reverse("dictionary:word_detail", args=(saved_word.id,))
        )
        self.assertContains(response, "apple")
        self.assertContains(response, "The fruit of an apple tree.")


class DeleteWordTests(TestCase):
    # Deleting a word removes it and goes back to My Vocabulary
    def test_delete_word(self):
        saved_word = create_word("apple")
        response = self.client.post(
            reverse("dictionary:delete_word", args=(saved_word.id,))
        )
        self.assertRedirects(response, reverse("dictionary:word_list"))
        self.assertFalse(Word.objects.filter(pk=saved_word.id).exists())
