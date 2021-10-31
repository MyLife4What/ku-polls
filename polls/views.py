"""App views for polls."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class IndexView(generic.ListView):
    """ListView on index page that contain queryset."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions.

        (not including those set to be published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """Detail view on detail page."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Detail view on results page."""

    model = Question
    template_name = 'polls/results.html'


@login_required()
def vote(request, question_id):
    """Vote page for the selected question."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if question.vote_set.filter(user=request.user).exists():
            the_vote = question.vote_set.get(user=request.user)
            the_vote.choice = selected_choice
            the_vote.save()
        else:
            selected_choice.vote_set.create(user=request.user, question=question)
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))


def detail(request, question_id=None):
    """Detail page for the selected question."""
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, "Poll not available")
        return HttpResponseRedirect(reverse('polls:index'))
    else:
        return render(request, 'polls/detail.html', {'question': question, })
