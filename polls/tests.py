"""Test for function in polls."""
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


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


def create_question(question_text, days):
    """
    Create a question.

    with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    """Test for question index view."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """The detail view of a question.

        with a pub_date in the past displays the question's text.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """The detail view of a question.

        with a pub_date in the future returns a 404 not found.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist.

        only past questions are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    """Test Question class in models.py."""

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 302 not found.
        """
        future_question = create_question(question_text='Future question.',
                                          days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.',
                                        days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)