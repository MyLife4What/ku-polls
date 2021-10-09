"""Models creation for polls."""
import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Question models for polls.

    Parameter:
        models: Question models(question text, publication date, end date)
    """

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('ending date for voting', null=True, default=timezone.now)

    def __str__(self):
        """Return question text."""
        return self.question_text

    def was_published_recently(self):
        """Check that question was not published more than one day.

        Returns:
            bool: True if question was not published more than one day.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        """Check that current date is on or after question’s publication date.

        Returns:
            bool: True if question was published.
        """
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """Check that voting is currently allowed for this question.

        Return:
            bool: True if question is now open.
        """
        now = timezone.now()
        return self.end_date >= now >= self.pub_date


class Choice(models.Model):
    """Choice models for polls.

    Returns:
        models: Choice models(question, choice text, votes)

    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return choice text."""
        return self.choice_text
