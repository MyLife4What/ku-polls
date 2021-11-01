"""Test for polls model and dates."""
import datetime

from django.test import TestCase
from django.utils import timezone
from polls.models import Question


def create_question(question_text, days):
    """Create a question with the given `question_text`.

    Args:
        question_text
        days
    Returns: Question object
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    """Test for question models."""

    def test_was_published_recently_with_future_question(self):
        """Check function was_published_recently().

        It should returns False for questions which pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Check function was_published_recently().

        It should returns False for questions
        which pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Check function was_published_recently().

        It should returns True for questions
        which pub_date is within the last day.
        """
        time = timezone.now() - \
            datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_previous_question(self):
        """Check function is_published().

        It should returns True for question that pub_date is in the past.
        """
        time = timezone.now() - datetime.timedelta(days=10)
        previous_question = Question(pub_date=time)
        self.assertIs(previous_question.is_published(), True)

    def test_is_published_with_upcoming_question(self):
        """Check function is_published().

        It should returns False for question that pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(hours=12)
        upcoming_question = Question(pub_date=time)
        self.assertIs(upcoming_question.is_published(), False)

    def test_can_vote_with_previous_question(self):
        """Check that can_vote() returns False for question that closed."""
        time = timezone.now() - datetime.timedelta(days=5)
        end_time = timezone.now() - datetime.timedelta(days=3)
        previous_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(previous_question.can_vote(), False)

    def test_can_vote_with_upcoming_question(self):
        """Check function can_vote().

        It should returns False for question that not opened yet.
        """
        time = timezone.now() + datetime.timedelta(days=10)
        end_time = timezone.now() + datetime.timedelta(days=30)
        upcoming_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(upcoming_question.can_vote(), False)
