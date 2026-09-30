from django.db import models
from django.utils import timezone


# A saved word; Django turns this class into a table in db.sqlite3
class Word(models.Model):
    word = models.CharField(max_length=100)
    definition = models.TextField()
    # Used to show the newest words first
    date_saved = models.DateTimeField("date saved", default=timezone.now)
    # False = Pending, True = Learned
    is_learned = models.BooleanField(default=False)

    # Text shown for each word, for example in the admin site
    def __str__(self):
        return self.word
