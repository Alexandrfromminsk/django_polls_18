from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader, RequestContext
from .models import Choice, Question

def index(request):
    latest_questions_list = Question.objects.order_by('-pub_date')[:10]
    template = loader.get_template("polls/index.html")
    context = RequestContext(request, {
        'latest_question_list': latest_questions_list,
    })

    return HttpResponse(template.render(context))

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse_lazy('polls:results', args=(p.id,)))

