from django.db import models
from django.utils import timezone


class Word(models.Model):
    """
    A word saved by the user. Django turns this class into a table
    in the database (db.sqlite3), and each saved word is one row.
    """

    # The English word, for example "serendipity".
    word = models.CharField(max_length=100)

    # Its definition. TextField is used because definitions can be long.
    definition = models.TextField()

    # When the word was saved. Used to show the newest words first.
    date_saved = models.DateTimeField("date saved", default=timezone.now)

    # False while the user is still learning the word, True when they know it.
    is_learned = models.BooleanField(default=False)

    def __str__(self):
        return self.word
