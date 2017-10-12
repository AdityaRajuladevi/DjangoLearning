from django.views import generic
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question
from django.shortcuts import get_object_or_404,render
from django.urls import reverse

# Create your views here.
def index(request):
    latest_question_list=Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    """template=loader.get_template('polls/index.html')
    return HttpResponse(template.render(context,request))
    """
    return render(request,'polls/index.html',context)

def detail(request,question_id):
    """
    try:
        question=Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request,'polls/details.html',{'question':question})
    """
    question=get_object_or_404(Question,pk=question_id)
    return render(request,'polls/details.html',{'question':question})

def results(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request,'polls/results.html',{'question':question})


# here onwards generic views example

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'

class ResultsView(generic.DetailView):
    model=Question
    template_name = 'polls/results.html'


def vote(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except:
        return render(request,'polls/details.html',{'question':question,'error_message':"You didn't select a choice.",})
    else:
        print(selected_choice)
        selected_choice.votes+=1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))