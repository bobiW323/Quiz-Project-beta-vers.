from django.shortcuts import render, get_object_or_404

from django.http import HttpResponseRedirect

from django.urls import reverse
from django.utils import timezone

from .models import Question, Choice, User, Questionnaire


def front_page(request):
    return render(request, 'quizmonkey/front_page.html')


def main_page(request):
    return render(request, 'quizmonkey/main_page.html')


def index(request):
    all_entries = Questionnaire.objects.all()
    context = {
        'questionnaires': all_entries,
    }
    return render(request, 'quizmonkey/index.html', context)


def get_questionnaire(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_id)
    questions = questionnaire.question_set.all()
    latest_question_list = questions.order_by('is_checkbox')[:]
    context = {
        'latest_question_list': latest_question_list,
        'title': questionnaire.title,
        'count': latest_question_list.count(),
    }
    return render(request, 'quizmonkey/question.html', context)


def submit_vote(request):
    values = request.POST.items()
    q = User(pub_date=timezone.now())
    for k, v in values:
        if len(k) > 9 and k[:8] == 'question' and k[-2:] != '[]':
            question = get_object_or_404(Question, pk=int(k[9:]))
            try:
                selected_choice = question.choice_set.get(pk=int(v))
            except (KeyError, Choice.DoesNotExist):
                print("can't find")
            else:
                selected_choice.votes += 1
                if selected_choice.is_answer:
                    q.grade += 1
                selected_choice.save()
        elif len(k) > 9 and k[:8] == 'question' and k[-2:] == '[]':
            list = request.POST.getlist(k)
            question = get_object_or_404(Question, pk=int(k[9:10]))
            for value in list:
                try:
                    selected_choice = question.choice_set.get(pk=int(value))
                except (KeyError, Choice.DoesNotExist):
                    print("can't find")
                else:
                    selected_choice.votes += 1
                    selected_choice.save()
        else:
            q.__setattr__(k, v)
    q.save()
    return HttpResponseRedirect(reverse('index'))


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'quizmonkey/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'quizmonkey/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'quizmonkey/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('quizmonkey:results', args=(question.id,)))
